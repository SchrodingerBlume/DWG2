# import csv

# # 配置区（用户需要修改的部分）
# input_file = 'data big\data_1.6w行.csv'        # 输入文件名
# output_file = '4.1_data.csv'      # 输出文件名
def extract_rows(input_file, output_file, target_rows):
    # 转换行号为0-based索引并保留原始顺序
    original_order = [rn  for rn in target_rows]
    # original_order = [rn - 1 for rn in target_rows]
    target_set = set(original_order)
    
    row_dict = {}
    
    with open(input_file, 'r') as infile:
        for current_line_num, line in enumerate(infile):
            if current_line_num in target_set:
                row_dict[current_line_num] = line
                # 提前退出循环如果已找到所有目标行
                if len(row_dict) == len(target_set):
                    break
    
    # 按原始顺序输出
    output_lines = [row_dict[rn] for rn in original_order]
    
    with open(output_file, 'w') as outfile:
        outfile.writelines(output_lines)

# 示例使用
if __name__ == "__main__":
    # emt相关rna
    emt=[12479, 8990, 2838, 11429, 10842, 14613, 2255, 5858, 12197, 8128, 9038, 5707, 7081, 1827, 13421, 13804, 13438, 11625, 12763, 6154, 11096, 13424] 
    # 其他排名前50的rna
    your_row_numbers = [410,14249,15621,15623,15620,15616,13111,10942,15617,15613,10993,2527,12747,10336,7740,14807,2440,15614,5717,4104,4491,4723,700,14596,10880,14268,11067,5054,11548,10379,14705,10292,15612,601,8858,5228,5053,1814,13151,5025,12566,10416,12436,5660,2602,9543,15618,15611,5024,2829,7503,4997,4716,1440,14786,8925,1501,849,10732,1001,3876,4326,2456,4988,1835,9870,7239,1008,1798,13981,9906,2441,2045,14242,11710,13798,3016,9781,13178,2042,10603,12030,8139,15486,10227,8493,12095,2041,1002,904,2279,1721,9649,6390,15124,4383,2531,6750,7373,14713]
    # CLDN7,VIM,CDH1
    # other3=[12479,8990,12197]
    emt.extend(your_row_numbers)
    # emt.extend(other3)
    
    extract_rows(
        input_file='data big\data_1.6w行.csv',
        output_file='GNN部分\\4.1_data.csv',
        target_rows=emt
    )