import pandas as pd
import numpy as np
import torch
from torch_geometric.nn import GCNConv, GAE
from torch_geometric.data import Data
from torch.optim.lr_scheduler import ReduceLROnPlateau


# 检查GPU是否可用
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# 数据加载

print("读取降维后数据")
path1 = "data_1.6w行.降维.csv"
feature = pd.read_csv(path1, header=None)
# 转换为Tensor并移动到设备（优化为float32类型）
feature_tensor = torch.tensor(feature.values, dtype=torch.float32).to(device)

print("读取graph结构")
df = pd.read_csv('graph2_abs_0.5_前两列.csv', header=None, names=['source', 'target', ''])

print("优化edge_index创建")
# 合并为单一numpy数组再转换
edge_array = np.stack([df['source'].values, df['target'].values], axis=0)  # 形状 (2, N)
edge_index = torch.as_tensor(edge_array, dtype=torch.long).contiguous().to(device)

print("组织data")
data = Data(x=feature_tensor, edge_index=edge_index).to(device)

# 定义GAE模型（保持不变）
class Encoder(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(256, 256)
        self.conv2 = GCNConv(256, 128)
        self.conv3 = GCNConv(128, 64)  # 增加第三层
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index).relu()
        return self.conv3(x, edge_index)

model = GAE(Encoder()).to(device)
# 优化器和学习率调度
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=20)

# 训练循环（添加验证监控）
for epoch in range(200):
    model.train()
    optimizer.zero_grad()
    z = model.encode(data.x, data.edge_index)
    loss = model.recon_loss(z, data.edge_index)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
    optimizer.step()
    scheduler.step(loss)  # 动态调整学习率
    if (epoch + 1) % 10 == 0:
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')
    

print("生成嵌入关系")
embeddings = model.encode(data.x, data.edge_index).detach().cpu()


# 找到其他与emt相关的物质
import torch

# 假设已知10种物质的索引为 known_indices (列表)
known_indices = [224,716,830,1460,1514,1589,1931,1995,2128,2255,2256,2547,2548,2786,3018,3908,4518,4537,5021,6157,7716,8641,9037,9038,9404,9507,10767,10950,11096,11356,11429,12008,12039,12070,12350,12737,13421,13438,13446,13716,13872,13958,14103,14592,14613,14827,15360,15395]  # 示例索引
known_embeddings = embeddings[known_indices]  # 提取已知嵌入

# 聚合方法：均值（或加权均值、最大池化等）
query_embedding = torch.mean(known_embeddings, dim=0)  # 形状 [embedding_dim]


from sklearn.metrics.pairwise import cosine_similarity

# 计算余弦相似度（或欧氏距离）
similarities = cosine_similarity(query_embedding.unsqueeze(0), embeddings)
similarities = similarities.flatten()  # 形状 [16000]

# 按相似度排序
sorted_indices = torch.argsort(torch.tensor(similarities), descending=True)


# 排除已知的10种物质
candidates = []
for idx in sorted_indices:
    if idx.item() not in known_indices:
        candidates.append(idx.item())
    if len(candidates) >= 100:  # 取Top 100候选
        break
pathOut="候选物质index相关性高到低排序.txt"
with open(pathOut,'w') as outfile:
    for index in candidates:
        outfile.write(f"{index},")
print("Top候选物质索引:", candidates[:20])  # 示例输出前20