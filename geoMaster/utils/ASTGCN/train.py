from torch_geometric.loader import DataLoader
from graph_data import get_dataset
from model import ASTGCN_with_GAT  # 使用 GAT 模型
import torch
from torch.optim import Adam
import torch.nn.functional as F
from torch.utils.data import random_split
from sklearn.preprocessing import StandardScaler
import joblib

# 配置
csv_path = './data/labels.csv'
image_dir = './data/images'
num_classes = 3
in_channels = 3  # 每个时间段的特征数
out_channels = 1024
epochs = 200  # 增加训练轮数
batch_size = 16  # 修改批次大小
lr = 1e-4  # 使用较小的学习率
dropout = 0.3  # Dropout 概率

# 检查是否可以使用GPU，如果可以，使用CUDA
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 加载数据集
dataset = get_dataset(csv_path, image_dir)

# 计算类别权重
label_counts = [0, 0, 0]  # 假设数据集有3个类别
for data in dataset:
    label_counts[data.y.item()] += 1

#print(f"label_counts: {label_counts}")


total_samples = sum(label_counts)
weights = [total_samples / (3 * count) if count != 0 else 0 for count in label_counts]
weights = torch.tensor(weights, dtype=torch.float).to(device)

# 80% 训练集，20% 测试集
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size

train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

# 创建 DataLoader
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 初始化模型、优化器
model = ASTGCN_with_GAT(in_channels, out_channels, num_classes, dropout).to(device)

optimizer = Adam(model.parameters(), lr=lr, weight_decay=1e-5)  # 添加 L2 正则化
criterion = torch.nn.CrossEntropyLoss(weight=weights)

# 学习率衰减
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.7)

# 标准化器
scaler = StandardScaler()

# 训练过程
for epoch in range(epochs):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    for data in train_loader:
        data = data.to(device)

        # 提取特征并进行标准化
        features = data.x.cpu().numpy()

        # 使用 scaler 计算并标准化训练数据
        features = scaler.fit_transform(features)  # 使用 fit_transform 对训练数据进行标准化
        data.x = torch.tensor(features, dtype=torch.float).to(device)

        optimizer.zero_grad()
        out = model(data.x, data.edge_index, data.batch)  # 传递 batch 信息
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = out.max(dim=1)
        correct += predicted.eq(data.y).sum().item()
        total += data.y.size(0)

    # 更新学习率
    scheduler.step()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader)}, Accuracy: {correct/total}")

    # 保存标准化器
    joblib.dump(scaler, 'scaler.pkl')  # 保存 scaler，供测试时使用

# 测试过程
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for data in test_loader:
        data = data.to(device)

        # 提取特征并进行标准化
        features = data.x.cpu().numpy()
        scaler = joblib.load('scaler.pkl')  # 加载保存的 scaler
        features = scaler.transform(features)  # 使用相同的标准化器
        data.x = torch.tensor(features, dtype=torch.float).to(device)

        out = model(data.x, data.edge_index, data.batch)
        _, predicted = out.max(dim=1)
        correct += predicted.eq(data.y).sum().item()
        total += data.y.size(0)

print(f"Test Accuracy: {correct / total}")

# 保存超参数和模型权重
checkpoint = {
    'model_state_dict': model.state_dict(),
    'out_channels': out_channels,
}

# 保存模型
torch.save(checkpoint, 'new_astgcn_with_gat_model.pth')
