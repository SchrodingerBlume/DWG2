# 读取index.csv中的行号
path1='GNN部分\\3.1_ 候选物质index相关性高到低排序.txt'
path2="GNN部分\\3.2_ 候选物质index相关性高到低排序.txt.txt"
pathData='GNN部分\data\\1.6w行第一列.txt'
with open(path1, 'r') as f:
    line= f.readline()
    print(line)
    ll= line.split(",")
    indices=[]
    for l in ll:
        # print(l)
        indices.append(int(l))

# 读取data.txt的所有行
with open(pathData, 'r') as f:
    data_lines = f.readlines()

# 收集对应行内容（处理行号越界）
output = []
for idx in indices:
    if 0 < idx < len(data_lines):
        output.append(data_lines[idx])
    else:
        print(f"行号 {idx} 无效，已跳过")

# 输出结果到控制台
# print(''.join(output), end='')

# 或者写入到文件（例如output.txt）
with open(path2, 'w') as f:
    f.writelines(output)