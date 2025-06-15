import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd

# 文件路径和参数设置
file_path = 'dataset/WIFIUAV_2460'
fs = 30000000  # 采样频率(Hz)
seg_len = 1.5e6  # 每段的长度
#label = 'wifiuav'  # 标签
output_dir = 'data/images'  # 存图和标签的目录

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 读取二进制数据并将其重组成复数格式
data = np.fromfile(file_path, dtype=np.float32)
value = data[::2] + 1j * data[1::2]  # 复数重组

# 计算总的段数
n_seg = int(np.floor(len(value) / seg_len))

# 初始化文件名和标签
filenames = []
#labels = [label] * n_seg

# 遍历每一段数据并处理
for i in range(n_seg):
    # 截取每段数据
    idx0 = int((i) * seg_len)
    idx1 = int((i + 1) * seg_len)
    x = value[idx0:idx1]

    # 归一化
    N = len(x)
    t = np.arange(N) / fs
    x_norm = np.real(x) / np.max(np.abs(np.real(x)))  # 归一化到 [-1, 1] 范围

    # 绘制时域图
    plt.figure(figsize=(6, 2))
    plt.plot(t, x_norm, linewidth=1)
    plt.grid(True)
    plt.xlim([0, N / fs])

    # 保存图像
    fname = f"seg_{i + 226:04d}.png"  # 图像文件名
    full_path = os.path.join(output_dir, fname)
    plt.savefig(full_path, dpi=50, bbox_inches='tight')
    plt.close()

    filenames.append(fname)



print(f'共生成 {n_seg} 张图，保存在 "{output_dir}"；')
