target_prefixes =["WIFI","WNT","CATENIN","TCF","LEF","ZEB1","ZEB2","TGF","AKT","PI3K","SMAD2","SMAD3","SMAD4","SRC","HAWAI","ARF6","INTEGRIN","FAK"]  # 需要检测的多个开头字符串

path1="第一列.txt"
path2="第一列.select.txt"
with open(path1, 'r') as infile, open(path2, 'w') as outfile:
    re=""
    for line_number, line in enumerate(infile, start=0):  # 行号从1开始计数
        if line.startswith(tuple(target_prefixes)):
            re+=","+str(line_number)
            outfile.write(f"{line_number},{line}")
    outfile.write(re)