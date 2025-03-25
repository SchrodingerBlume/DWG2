import pandas as pd
path="filtered_normalized_expression.csv"
path2="filtered_normalized_expression4.csv"
import csv
from itertools import islice

def get_column_count(path):
    """获取CSV总列数"""
    with open(path, 'r') as f:
        reader = csv.reader(f)
        return len(next(reader))

def transpose_large_csv_chunked(path, path2, chunk_size=10):
    total_columns = get_column_count(path)
    
    with open(path2, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # 分块处理列 (0, chunk_size, 2*chunk_size...)
        for start_col in range(0, total_columns, chunk_size):
            end_col = min(start_col + chunk_size, total_columns)
            current_chunk_size = end_col - start_col
            
            # 初始化存储容器: 每个列的数据存为一个列表
            chunk_data = [[] for _ in range(current_chunk_size)]
            
            # 读取文件一次，收集当前块的所有列数据
            with open(path, 'r') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    # 遍历当前块的每一列
                    for i in range(current_chunk_size):
                        col_idx = start_col + i
                        # 处理列索引越界的情况（如某些行列数不足）
                        if col_idx < len(row):
                            chunk_data[i].append(row[col_idx])
                        else:
                            chunk_data[i].append('')  # 填充空值
            
            # 将当前块的多列数据写入输出文件
            for col_data in chunk_data:
                writer.writerow(col_data)


# 设置块大小为20列（根据内存调整）
transpose_large_csv_chunked(path, path2, chunk_size=200)