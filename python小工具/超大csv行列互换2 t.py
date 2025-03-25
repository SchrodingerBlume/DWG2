import csv
import os

def transpose_large_file(input_path, output_path, chunk_size=1000):
    print("step1")
    # 创建临时目录
    temp_dir = 'temp_transpose_8w_16w'
    os.makedirs(temp_dir, exist_ok=True)
    temp_files = []
    print("step2")

    # 确定总行数和列数
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        first_row = next(reader)
        num_cols = len(first_row)
        num_rows = 1  # 已读取第一行
        for _ in reader:
            num_rows += 1
    print("step3")

    print(f"转置开始，原文件共{num_rows}行，{num_cols}列。")

    # 分块处理原文件
    with open(input_path, 'r') as f_in:
        reader = csv.reader(f_in)
        for chunk_idx in range(0, num_rows, chunk_size):
            # 读取块数据
            rows = []
            for _ in range(chunk_size):
                try:
                    rows.append(next(reader))
                except StopIteration:
                    break
            if not rows:
                break
            
            # 转置当前块
            transposed = list(zip(*rows))
            # 写入临时文件
            temp_path = os.path.join(temp_dir, f'temp_{chunk_idx//chunk_size}.csv')
            temp_files.append(temp_path)
            with open(temp_path, 'w', newline='') as f_out:
                writer = csv.writer(f_out)
                writer.writerows(transposed)
            print(f"已处理块 {chunk_idx//chunk_size}，包含 {len(rows)} 行。")

    # 合并临时文件
    with open(output_path, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        # 打开所有临时文件的读取器
        readers = [csv.reader(open(file, 'r')) for file in temp_files]
        # 逐行合并
        for j in range(num_cols):
            merged_row = []
            for reader in readers:
                try:
                    row = next(reader)
                    merged_row.extend(row)
                except StopIteration:
                    continue  # 处理文件行数不一致
            writer.writerow(merged_row)
            if j % 1000 == 0:
                print(f"已写入转置后的第 {j} 行，共 {num_cols} 行。")
    
    print("请手动清理临时文件")
    # 清理临时文件
    # for file in temp_files:
    #     os.remove(file)
    # os.rmdir(temp_dir)
    # print("转置完成，输出文件已保存至", output_path)


path="GNN部分\\4.1_data.csv.T.csv.T.csv"
path2=path+".T.csv"
# 使用示例
transpose_large_file(path, path2)