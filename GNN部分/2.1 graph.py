import pandas as pd
from scipy.stats import spearmanr
import numpy as np

# 行变为样本，列变为化学物质，以便计算列之间的相关系数
# 1.6万行是rna
print("开始读取")
data_transposed = pd.read_csv('data_1.6w行.csv', header=None)
print("读取完毕")
# 计算所有化学物质之间的Spearman相关系数及p值矩阵
corr_matrix, p_matrix = spearmanr(data_transposed, axis=0)
print("计算完毕")
# 生成边列表，假设只保留非对角线的边，并筛选p值显著的相关系数（例如p < 0.05）
edges = []
n = corr_matrix.shape[0]  # 化学物质的数量

for i in range(n):
    for j in range(i + 1, n):  # 仅上三角部分，避免重复和自环
        corr = corr_matrix[i, j]
        p_val = p_matrix[i, j]
        if p_val < 0.05:  # 可根据需要调整p值阈值
            if abs(corr)>0.2:
                edges.append((i, j, corr, p_val))

print("开始保存到csv")
# 保存边列表到CSV
edges_df = pd.DataFrame(edges, columns=['Chemical1', 'Chemical2', 'Correlation', 'P-value'])
edges_df.to_csv('graph2.csv', index=False)