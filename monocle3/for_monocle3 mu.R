# install.packages("BiocManager")
# BiocManager::install("monocle3")

# 加载必要的包
library(monocle3)
library(dplyr)
library(ggplot2)

# 设置工作目录（可选）
# setwd("D:/Cambridge/monocle3")

print("加载lib完毕===============================")

# 读取数据
# data_path <- "D:/Cambridge/monocle3/filtered_expression_for_monocle3.csv"
data_path <- "H:/_python/DWG2/GNN部分/4.1_data.csv.T.csv.T_mu.csv.T.csv.归一化.csv"
print("开始读取csv")

expression_data <- read.csv(data_path, row.names = 1,check.names = FALSE)
print("读取完毕")
# print(colnames(expression_data))  # 输出所有列名

# 准备cell_metadata（样本信息）
cell_metadata <- data.frame(
  row.names = rownames(expression_data),
  mu = expression_data$mu
)
print(" 准备cell_metadata 完毕")

# 准备gene_metadata（基因信息）
genes_of_interest <- c("CDH1","VIM","CLDN7","WNT4","TGFBR3","WNT2B","TGFB2","WNT9A","AKT3","TGFA","TCF7L1","TGFBRAP1"
,"ZEB2","ZEB2-AS1","WNT6","WNT10A","TGFBR2","WNT5A","LEF1","TCF7","TGFBI","TCF19","WNT2","TGFBR1","WNT11","ZEB1-AS1","ZEB1"
,"TCF7L2","WNT5B","ARF6","TGFB3","AKT1","TCF12","SMAD3","SRCAP","TGFB1I1","AKTIP","TCF25","SRCIN1","SMAD2","SMAD4","TCF4"
,"SRC","TCFL5","TCF3","TGFBR3L","AKT2","TGFB1","AKT1S1","TCF20","WNT7B","RBPMS","IFITM3","GSN","IGFBP4","COL18A1","COX7A1"
,"PTRF","PRKCDBP","TIMP3","COL4A2","COL4A1","CD63","IFI27","EHD2","SPARCL1","WDR13","IGFBP7","ADAMTS1","UACA","NNMT"
,"LAMB2","TINAGL1","CAV2","A2M","CAV1","PLK2","CRIP2","PLPP1","BCAM","ID3","GNG11","OLFML2A","COL15A1","SWAP70"
,"ABCD4","LUZP1","SNRK","PRSS23","HES4","HOXD9","SOCS2","STC1","CLDN15","DOCK9","SCARB1","ARL2","RASIP1","NR2F2"
,"EFNB2","PTPRM","PIK3C2A","ITGA1","GUCY1A3","SMAGP","EPS8","TGM2","DOCK6","ZNF280D","ADGRG1","HEY1","SERPING1"
,"LAMA5","ANGPT2","TNFAIP1","MYO1B","NOTCH1","PHACTR2","C4orf32","RAPGEF5","CD200","MTUS1","SH2D3C","PICALM"
,"IPO11","YPEL2","PTK2","SLC9A3R2","SMAD1","PLXND1","LMCD1","SERPINB6","NES","CYB5R3","LIMS2","MOB2","SEPT4"
,"ESAM","AK1","TNS2","RHOC","PGF","SLC29A1","TMEM88","FZD4","RAB13","C1orf54","ECE1","NOSTRIN","DLL4","HEG1")
print(" 准备基因信息 完毕")

gene_metadata <- data.frame(
  row.names = genes_of_interest,
  gene_short_name = genes_of_interest
)
print(" 准备gene_metadata 完毕")

# 准备表达矩阵
expression_matrix <- t(expression_data[, genes_of_interest])
print(" 准备表达矩阵 完毕")

# 创建CDS对象
cds <- new_cell_data_set(
  expression_data = as.matrix(expression_matrix),
  cell_metadata = cell_metadata,
  gene_metadata = gene_metadata
)
print(" 创建CDS对象 完毕")
print("继续运行1")

# stop()
print("预处理数据")
# 预处理数据
cds <- preprocess_cds(cds, num_dim = 10)
print("降维")
# 降维
cds <- reduce_dimension(cds, reduction_method = "UMAP")
print("聚类")
# 聚类
cds <- cluster_cells(cds, k = 20)
print("学习轨迹")
# 学习轨迹
cds <- learn_graph(cds)

print("基于mlr确定轨迹的起点")
# 基于mlr确定轨迹的起点
# 选择mlr最低的细胞作为起点（表示上皮状态）
mu_values <- colData(cds)$mu
start_cell <- which.min(mu_values) 
cds <- order_cells(cds, root_cells = rownames(colData(cds))[start_cell])


print("可视化UMAP")
dir="H:/_python/DWG2/monocle3/"
f1=paste0(dir, "UMAP2.pdf")
print(f1)
# 可视化
# 1. 基本的UMAP图
pdf(f1, width = 8, height = 6)
plot_cells(cds, 
           color_cells_by = "pseudotime",
           label_cell_groups = FALSE,
           label_leaves = FALSE,
           label_branch_points = FALSE)
dev.off()
print("可视化完毕")
# stop();

# print("可视化UMAP2")

# # 2. 带轨迹的UMAP图
# pdf("D:/Cambridge/monocle3/monocle3_trajectory.pdf", width = 8, height = 6)
# plot_cells(cds,
#            color_cells_by = "pseudotime",
#            label_cell_groups = FALSE,
#            label_leaves = FALSE,
#            label_branch_points = FALSE,
#            graph_label_size = 1.5)
# dev.off()

# # 3. 修改后的基因表达图绘制代码
# for (gene in genes_of_interest) {
#   pdf(paste0("D:/Cambridge/monocle3/gene_", gene, "_pseudotime.pdf"), width = 8, height = 6)
#   print(plot_genes_in_pseudotime(cds[gene,], 
#                                  color_cells_by = "pseudotime"))
#   dev.off()
# }

# # 获取pseudotime值
# pseudotime_values <- pseudotime(cds)

# # 创建新的整合数据框
# # 1. 添加pseudotime列到原始数据
# integrated_data <- expression_data
# integrated_data$pseudotime <- pseudotime_values

# # 2. 按pseudotime排序
# integrated_data <- integrated_data[order(integrated_data$pseudotime), ]

# # 3. 计算每个基因与pseudotime的相关性
# correlations <- sapply(genes_of_interest, function(gene) {
#   cor(integrated_data[[gene]], integrated_data$pseudotime, 
#       method = "spearman", use = "complete.obs")
# })

# # 创建相关性数据框
# correlation_df <- data.frame(
#   gene = genes_of_interest,
#   pseudotime_correlation = correlations
# )

# # 保存结果文件
# # 1. 保存整合后的数据（包含所有原始数据和新添加的pseudotime）
# write.csv(integrated_data, 
#           "D:/Cambridge/monocle3/integrated_data_with_pseudotime.csv", 
#           row.names = TRUE)

# # 2. 保存基因相关性数据
# write.csv(correlation_df, 
#           "D:/Cambridge/monocle3/gene_pseudotime_correlations.csv", 
#           row.names = FALSE)

# # 输出处理结果的简要统计
# cat("数据处理完成！\n")
# cat("生成的文件：\n")
# cat("1. integrated_data_with_pseudotime.csv - 包含", nrow(integrated_data), "行,", ncol(integrated_data), "列\n")
# cat("2. gene_pseudotime_correlations.csv - 包含", nrow(correlation_df), "个基因的相关性数据\n")
# cat("3. 生成了", length(genes_of_interest), "个基因的表达趋势图\n")

# # 展示相关性结果
# print("基因与伪时间的相关性（从高到低排序）：")
# correlation_df_sorted <- correlation_df[order(-abs(correlation_df$pseudotime_correlation)), ]
# print(correlation_df_sorted)

# # 保存详细的分析报告
# sink("D:/Cambridge/monocle3/analysis_report.txt")
# cat("EMT轨迹分析报告\n")
# cat("================\n\n")
# cat("1. 数据概况：\n")
# cat("   - 总细胞数：", nrow(integrated_data), "\n")
# cat("   - 分析基因数：", length(genes_of_interest), "\n\n")
# cat("2. 伪时间分析结果：\n")
# cat("   - 伪时间范围：", min(pseudotime_values), "至", max(pseudotime_values), "\n\n")
# cat("3. 基因相关性分析：\n")
# print(correlation_df_sorted)
# cat("\n4. 输出文件列表：\n")
# cat("   - integrated_data_with_pseudotime.csv\n")
# cat("   - gene_pseudotime_correlations.csv\n")
# cat("   - monocle3_umap.pdf\n")
# cat("   - monocle3_trajectory.pdf\n")
# cat("   - 各基因表达趋势图\n")
# sink()
