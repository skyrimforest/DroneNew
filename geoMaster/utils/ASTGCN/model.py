import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool

class ASTGCN_with_GAT(nn.Module):
    def __init__(self, in_channels, out_channels, num_classes, dropout=0.2):
        super(ASTGCN_with_GAT, self).__init__()

        # 增加更多层数，使用跳跃连接
        self.gat1 = GATConv(in_channels, out_channels, heads=4, dropout=dropout)
        self.gat2 = GATConv(out_channels * 4, out_channels, heads=4, dropout=dropout)
        self.gat3 = GATConv(out_channels * 4, out_channels, heads=4, dropout=dropout)
        self.fc = nn.Linear(out_channels * 4, num_classes)
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x, edge_index, batch):
        # 图注意力层，添加跳跃连接
        x1 = F.relu(self.gat1(x, edge_index))
        x1 = self.dropout(x1)

        x2 = F.relu(self.gat2(x1, edge_index))
        x2 = self.dropout(x2)

        x3 = F.relu(self.gat3(x2, edge_index))
        x3 = self.dropout(x3)

        # 残差连接
        x = x3 + x1  # 通过跳跃连接增加前层的信息

        # 全局池化
        x = global_mean_pool(x, batch)

        # 分类层
        x = self.fc(x)
        return x
