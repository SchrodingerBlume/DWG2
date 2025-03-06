import csv

# 读取原始 CSV 的某一行
input_file = "第一行.txt"
output_file = "第一列.txt"

with open(input_file, "r", newline="") as infile:
    reader = csv.reader(infile)
    target_row = next(reader)  # 读取第一行，可根据需要调整

# 将每个字段写入新文件的独立行（单列）
with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    for field in target_row:
        writer.writerow([field])  # 每个字段作为单独的行

print(f"已将 {input_file} 的一行转换为单列写入 {output_file}")