import pandas as pd
import numpy as np

path1 = "GNN部分\\5.3_data.csv"
path2 = "GNN部分\\5.6_data.归一化.csv"

# 读取数据
df = pd.read_csv(path1)

# 需要归一化的列
columns_to_normalize = ['CLDN7', 'VIM', 'CDH1']

# 提取数据到NumPy数组以加速计算
data = df[columns_to_normalize].values

# 计算每列的最小值和最大值
min_vals = data.min(axis=0)
max_vals = data.max(axis=0)
diffs = max_vals - min_vals

# 执行归一化
normalized = (data - min_vals) / diffs

# 处理常数列（除零情况），设为0
normalized[:, diffs == 0] = 0

# 将结果更新回DataFrame
df[columns_to_normalize] = normalized

# 保存结果
df.to_csv(path2, index=False)  