import pandas as pd

# 读取原始CSV文件
df = pd.read_csv('graph2.csv')

# 筛选Correlation大于0.5的行
filtered_df = df[abs( df['Correlation']) > 0.5]

# 保存到新CSV文件，不包含索引
filtered_df.to_csv('graph2_abs_0.5.csv', index=False)