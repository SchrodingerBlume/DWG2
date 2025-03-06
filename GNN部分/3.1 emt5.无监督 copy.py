import pandas as pd
import numpy as np
import torch
from torch_geometric.nn import GCNConv, GAE
from torch_geometric.data import Data
from torch.optim.lr_scheduler import ReduceLROnPlateau


# check gpu
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

print("data load  read 16w x 256")
path1 = "1.1_ 降维后 data_1.6w行.csv"
feature = pd.read_csv(path1, header=None)
feature_tensor = torch.tensor(feature.values, dtype=torch.float32).to(device)

print("read edge_index")
df = pd.read_csv('2.3_ graph2_abs_0.5_前两列.csv', header=None, names=['source', 'target', ''])
edge_array = np.stack([df['source'].values, df['target'].values], axis=0)
edge_index = torch.as_tensor(edge_array, dtype=torch.long).contiguous().to(device)

print("create  data")
data = Data(x=feature_tensor, edge_index=edge_index).to(device)


class Encoder(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(256, 256)
        self.conv2 = GCNConv(256, 128)
        self.conv3 = GCNConv(128, 64)  
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index).relu()
        return self.conv3(x, edge_index)

model = GAE(Encoder()).to(device)


optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=20)
# loop
for epoch in range(200):
    model.train()
    optimizer.zero_grad()
    z = model.encode(data.x, data.edge_index)
    loss = model.recon_loss(z, data.edge_index)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
    optimizer.step()
    scheduler.step(loss)  
    if (epoch + 1) % 10 == 0:
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

print("gen embeddings")
embeddings = model.encode(data.x, data.edge_index).detach().cpu()


import torch
known_indices = [224,716,830,1460,1514,1589,1931,1995,2128,2255,2256,2547,2548,2786]  # 示例索引
known_embeddings = embeddings[known_indices] 

query_embedding = torch.mean(known_embeddings, dim=0)  

from sklearn.metrics.pairwise import cosine_similarity

similarities = cosine_similarity(query_embedding.unsqueeze(0), embeddings)
similarities = similarities.flatten()  

sorted_indices = torch.argsort(torch.tensor(similarities), descending=True)


candidates = []
for idx in sorted_indices:
    if idx.item() not in known_indices:
        candidates.append(idx.item())
    if len(candidates) >= 100:  
        break
pathOut="other EMT RNA.txt"
with open(pathOut,'w') as outfile:
    for index in candidates:
        outfile.write(f"{index},")

print("Top候选物质索引:", candidates[:20])  