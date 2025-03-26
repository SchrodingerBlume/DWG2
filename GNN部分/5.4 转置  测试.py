import csv

p1="GNN部分\\5.3_data.csv"
p2="GNN部分\\5.4_data.csv"
# 读取原始CSV文件
with open(p1, 'r', newline='') as f_in:
    reader = csv.reader(f_in)
    rows = list(reader)

# 行列转置（使用zip函数）
transposed = list(zip(*rows))

# 写入转置后的CSV文件
with open(p2, 'w', newline='') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(transposed)

