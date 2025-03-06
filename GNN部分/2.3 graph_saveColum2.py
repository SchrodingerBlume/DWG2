import csv

path1="graph2_abs_0.5.csv"
path2="graph2_abs_0.5_前两列.csv"

with open(path1, 'r') as infile, open(path2, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # 读取表头并写入新表头
    headers = next(reader)
    writer.writerow(headers[:2])  # 只保留前两列标题
    
    for row in reader:
        try:
            writer.writerow(row[:2])   # 只写入前两列数据
        except:
            pass  # 跳过格式错误行