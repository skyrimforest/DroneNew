import torch
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from torch_geometric.data import Data
from geoMaster.utils.ASTGCN.model import ASTGCN_with_GAT  # 假设你的模型路径
import argparse
from PIL import Image
from sklearn.preprocessing import StandardScaler

PATH=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))

# 配置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path =PATH+'/astgcn_with_gat_model.pth'  # 修改为你的模型路径
dropout = 0
batch_size = 1
outputDir = PATH+'/test_images/'  # 保存图像的目录

# 确保输出目录存在
os.makedirs(outputDir, exist_ok=True)

# 加载训练好的模型
checkpoint = torch.load(model_path)
model = ASTGCN_with_GAT(in_channels=3,  # 定义 in_channels
                        out_channels=checkpoint['out_channels'],  # 从 checkpoint 中获取 out_channels
                        num_classes=3,
                        dropout=0).to(device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 1. 解析复数时域信号
def parse_complex_data(data):
    """
    将接收到的时域数据转换为复数形式
    """
    value = data[0::2] + 1j * data[1::2]  # 解析为复数形式
    return value


# 2. 归一化数据
def normalize_data(value):
    """
    对时域数据进行归一化到 -1 到 1 之间
    使用复数的实部，并将其归一化到 [-1, 1] 之间
    """
    real_part = np.real(value)  # 取复数的实部

    # 将实部归一化到 [-1, 1] 之间
    normalized_value = 2 * (real_part - np.min(real_part)) / (np.max(real_part) - np.min(real_part)) - 1

    return normalized_value


# 3. 生成时域图（268x101）
def generate_time_domain_plot(normalized_value, fs=30e6):
    """
    生成时域图并保存为图像，图像大小为 268x101
    """
    # 时间向量
    N = len(normalized_value)
    t = np.arange(N) / fs

    # 绘制时域图
    h = plt.figure(figsize=(6, 2))
    plt.plot(t, normalized_value, linewidth=1)
    plt.grid(True)
    plt.xlim([0, N / fs])

    # 保存为低分辨率图（50 dpi）
    fname = f"seg_{np.random.randint(1000, 9999)}.png"  # 随机生成文件名
    full_path = os.path.join(outputDir, fname)
    canvas = FigureCanvas(h)
    canvas.print_figure(full_path, dpi=50)
    plt.close(h)

    return full_path


# 4. 构建图数据并预测
def make_graph(x_feat):
    T, F = x_feat.shape
    x = torch.tensor(x_feat, dtype=torch.float)

    # 构造链式连接的边：T-1 到 T 之间
    edge_index = torch.tensor([
        [i for i in range(T - 1)] + [i + 1 for i in range(T - 1)],
        [i + 1 for i in range(T - 1)] + [i for i in range(T - 1)],
    ], dtype=torch.long)


    return Data(x=x, edge_index=edge_index)


def extract_features_from_image(img_path, T=50):
    # 读取图像并转换为灰度图
    img = Image.open(img_path).convert('L')
    arr = np.array(img)  # 形状：H x W
    signal = np.mean(arr, axis=0)  # 压缩高度，得到 1D 波形

    length = len(signal)
    seg_len = length // T

    features = []
    for i in range(T):
        seg = signal[i * seg_len: (i + 1) * seg_len]
        f1 = np.max(seg)
        f2 = np.mean(seg)
        f3 = np.sum(seg ** 2)  # 能量
        features.append([f1, f2, f3])

    # 对特征进行标准化
    features = np.array(features)
    scaler = StandardScaler()
    features = scaler.fit_transform(features)  # 标准化

    return features  # 形状：[T, F]


def predict_and_save(data_segment):
    """
    对时域数据进行预测，并保存时域图
    """
    # 解析数据并生成时频图
    complex_data = parse_complex_data(data_segment)
    normalized_data = normalize_data(complex_data)

    # 生成时域图并保存
    file_path = generate_time_domain_plot(normalized_data)

    # 提取特征并生成图数据结构
    features = extract_features_from_image(file_path)
    data = make_graph(features)

    # 转移到设备
    data = data.to(device)

    # 预测
    with torch.no_grad():
        out = model(data.x, data.edge_index, data.batch)  # 注意 batch 可能为 None
        _, predicted = out.max(dim=1)

    return predicted.item(), file_path


# 命令行输入处理
def main(input_file):
    # 读取输入文件
    data = np.fromfile(input_file, dtype=np.float32)  # 假设数据是以二进制格式存储的
    print(f"读取文件 {input_file} 成功，数据长度: {len(data)}")
    data = data[:3000000]

    # 预测并保存图像
    prediction, fname = predict_and_save(data)

    # 输出预测结果
    print(f"预测类别：{prediction}")
    print(f"保存的图像文件：{fname}")

    res={
        "class":prediction,
        "filename":fname
    }

    return res

if __name__ == "__main__":
    # 使用 argparse 处理命令行参数
    parser = argparse.ArgumentParser(description="时域信号处理与预测")
    parser.add_argument('input_file', type=str, help="输入文件的路径")
    args = parser.parse_args()

    # 调用 main 函数进行处理
    main(args.input_file)
