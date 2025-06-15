import os
import numpy as np
import pandas as pd
from PIL import Image
from torch_geometric.data import Data
import torch
from sklearn.preprocessing import StandardScaler

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

def make_graph(x_feat, label):
    T, F = x_feat.shape
    x = torch.tensor(x_feat, dtype=torch.float)

    # 构造链式连接的边：T-1 到 T 之间
    edge_index = torch.tensor([
        [i for i in range(T - 1)] + [i + 1 for i in range(T - 1)],
        [i + 1 for i in range(T - 1)] + [i for i in range(T - 1)],
    ], dtype=torch.long)

    y = torch.tensor(label, dtype=torch.long)
    return Data(x=x, edge_index=edge_index, y=y)

def get_dataset(csv_path, image_dir):
    df = pd.read_csv(csv_path)
    data_list = []

    for _, row in df.iterrows():
        img_path = os.path.join(image_dir, row['Filename'])
        label = row['Label']
        feat = extract_features_from_image(img_path)
        data = make_graph(feat, label)
        data_list.append(data)

    return data_list
