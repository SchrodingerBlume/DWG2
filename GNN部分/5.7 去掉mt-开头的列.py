import pandas as pd

p1="GNN部分\\5.6_data.归一化.csv"
p2="GNN部分\\5.7_data.归一化.无MT-.csv"

# 读取CSV文件
df = pd.read_csv(p1)

# 筛选不以"MT-"开头的列
filtered_columns = [col for col in df.columns if not col.startswith('MT-')]

# 保留目标列并保存到新文件
df[filtered_columns].to_csv(p2, index=False)