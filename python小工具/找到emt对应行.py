target_prefixes =["WIFI","WNT","CATENIN","TCF","LEF","ZEB1","ZEB2","TGF","AKT","PI3K","SMAD2","SMAD3","SMAD4","SRC","HAWAI","ARF6","INTEGRIN","FAK"]  # 需要检测的多个开头字符串

path1="GNN部分\data\\1.6w行第一列.txt"
path2="GNN部分\第一列.index.select.txt"
path3="GNN部分\第一列.name.select.txt"
with open(path1, 'r') as infile, open(path2, 'w') as outfile,open(path3, 'w') as outfile3:
    re=""
    re3=""
    for line_number, line in enumerate(infile, start=0):  # 行号从0开始计数
        if line.startswith(tuple(target_prefixes)):
            print(line)

            re+=","+str(line_number)
            outfile.write(f"{line_number},{line}")
            linel_=line.replace("\n","")
            re3+=","+str(linel_)
            outfile3.write(f"{line_number},{line}")
    outfile.write(re)
    outfile3.write(re3)