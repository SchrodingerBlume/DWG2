# 读取qq文件，建立名字到行号的映射
name_to_line = {}
PathSource="GNN部分\data\\1.6w行第一列.txt"
pathTo="GNN部分\data\emt相关"
pathOut=pathTo+".csv"
with open(PathSource, 'r') as qq_file:
    for line_number, line in enumerate(qq_file, start=0):
        name = line.strip()
        name_to_line[name] = line_number

# 读取ww文件中的名字
with open(pathTo, 'r') as ww_file:
    ww_content = ww_file.readline().strip()
    names = [name.strip() for name in ww_content.split(',')]

# 收集所有结果
results = []
for name in names:
    line = name_to_line.get(name)
    if line is not None:
        results.append(f"{line}")
    else:
        results.append(f"{name}: Not found in qq")

# 将结果合并为一行，并写入output文件
with open(pathOut, 'w') as out_file:
    out_file.write(", ".join(results))