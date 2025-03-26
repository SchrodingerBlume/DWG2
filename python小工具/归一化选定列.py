import pandas as pd

path1="GNN部分\\4.1_data.csv.T.csv"
path2=path1+".归一化.csv"
# 读取CSV文件
df = pd.read_csv(path1)

# 定义需要归一化的列
columns_to_normalize = ['CLDN7', 'VIM', 'CDH1']

# 对每列进行最小-最大归一化
for col in columns_to_normalize:
    min_val = df[col].min()
    max_val = df[col].max()
    if max_val != min_val:
        df[col] = (df[col] - min_val) / (max_val - min_val)
    else:
        # 处理常数列（所有值相同的情况）
        df[col] = 0  # 或者设为0.5，根据需求调整

# 输出结果到CSV文件
df.to_csv(path2, index=False)