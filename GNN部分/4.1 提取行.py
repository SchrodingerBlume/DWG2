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
    # 替换为实际的20个行号列表
    num1=[224,716,830,1460,1514,1589,1931,1995,2128,2255,2256,2547,2548,2786,3018,3908,4518,4537,5021,6157,7716,8641,9037,9038,9404,9507,10767,10950,11096,11356,11429,12008,12039,12070,12350,12737,13421,13438,13446,13716,13872,13958,14103,14592,14613,14827,15360,15395] 
    your_row_numbers = [7018,8039,7802,12783,15596,14503,12815,8119,15239,10554,10553,9885,11020,14758,3842,6534,3752,15472,11452,8785,2928,342,6152,9598,6153,4269,11114,4260,14684,239,5998,7822,7715,8153,10926,231,2852,8684,11,2358,10065,6978,6084,10527,10291,8456,14781,11622,10546,13315,8189,4244,4030,9813,9654,13721,14176,11355,12111,7159,8318,13862,6899,12629,2424,7977,5508,3922,5715,3140,6933,7851,8680,4282,13018,7344,11718,4000,3256,2687,4818,1105,15367,2209,8079,13009,8869,7855,9835,834,10935,5227,12510,8685,1031,949,216,2315,11242,3220]  # 示例行号（1-based）
    num1.extend(your_row_numbers)
    
    extract_rows(
        input_file='data big\data_1.6w行.csv',
        output_file='4.1_data.csv',
        target_rows=num1
    )