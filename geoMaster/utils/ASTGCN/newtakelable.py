import numpy as np
import os

# 文件路径和参数设置
file_path = 'dataset/WIFIUAV_2460'
fs = 30000000  # 采样频率(Hz)
seg_len = 1.5e6  # 每段的长度
output_dir = 'data/time_series'  # 存储时间序列数据的目录

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 读取二进制数据并将其重组成复数格式
data = np.fromfile(file_path, dtype=np.float32)
value = data[::2] + 1j * data[1::2]  # 复数重组

# 计算总的段数
n_seg = int(np.floor(len(value) / seg_len))

# 初始化文件名列表
filenames = []

# 遍历每一段数据并处理
for i in range(n_seg):
    # 截取每段数据
    idx0 = int((i) * seg_len)
    idx1 = int((i + 1) * seg_len)
    x = value[idx0:idx1]

    # 归一化
    x_norm = np.real(x) / np.max(np.abs(np.real(x)))  # 归一化到 [-1, 1] 范围

    # 保存时间序列数据为 npy 文件
    fname = f"seg_{i + 226:04d}.npy"  # 文件名
    full_path = os.path.join(output_dir, fname)
    np.save(full_path, x_norm)  # 保存实部时间序列数据为 npy 文件
    filenames.append(fname)

print(f'共生成 {n_seg} 张时间序列文件，保存在 "{output_dir}"；')
