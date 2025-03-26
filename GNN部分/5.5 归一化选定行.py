import pandas as pd
p1="GNN部分\\5.4_data.csv"
p2="GNN部分\\5.5_data.csv"

# 读取CSV文件，第一列作为行索引
df = pd.read_csv(p1, index_col=0)

# 指定需要归一化的行标签
genes_to_normalize = ['CLDN7', 'VIM', 'CDH1']

# 提取目标行数据
selected_rows = df.loc[genes_to_normalize]

# 执行Min-Max归一化（按行处理）
min_values = selected_rows.min(axis=1)
max_values = selected_rows.max(axis=1)
normalized_rows = (selected_rows - min_values) / (max_values - min_values)

# 更新原始数据中的对应行
df.update(normalized_rows)

# 保存结果到out.csv，保留行标签作为第一列
df.to_csv(p2, index=True)