# install.packages("BiocManager")
# BiocManager::install("monocle3")

# 加载必要的包
library(monocle3)
library(dplyr)
library(ggplot2)

# 设置工作目录（可选）
# setwd("D:/Cambridge/monocle3")

# 读取数据
data_path <- "H:/_python/DWG2/monocle3/filtered_expression_for_monocle3.csv"
expression_data <- read.csv(data_path, row.names = 1)

# 准备cell_metadata（样本信息）
cell_metadata <- data.frame(
  row.names = rownames(expression_data),
  emt_ratio = expression_data$emt_ratio
)

# 准备gene_metadata（基因信息）
genes_of_interest <- c("SNAI2", "VIM", "CDH1", "TGFB2", "SMAD7", "TGFB1", 
                       "TGFBR1", "TGFB3", "TWIST1", "SNAI1", "SMAD4", "ZEB1", 
                       "TGFBR2", "SMAD3", "ZEB2", "SMAD2", "TWIST2")
gene_metadata <- data.frame(
  row.names = genes_of_interest,
  gene_short_name = genes_of_interest
)

# 准备表达矩阵
expression_matrix <- t(expression_data[, genes_of_interest])

# 创建CDS对象
cds <- new_cell_data_set(
  expression_data = as.matrix(expression_matrix),
  cell_metadata = cell_metadata,
  gene_metadata = gene_metadata
)

# 预处理数据
cds <- preprocess_cds(cds, num_dim = 10)

# 降维
cds <- reduce_dimension(cds, reduction_method = "UMAP")

# 聚类
cds <- cluster_cells(cds)

# 学习轨迹
cds <- learn_graph(cds)

# 基于EMT比率确定轨迹的起点
# 选择EMT比率最高的细胞作为起点（表示上皮状态）
emt_ratio_values <- colData(cds)$emt_ratio
start_cell <- which.max(emt_ratio_values)
cds <- order_cells(cds, root_cells = rownames(colData(cds))[start_cell])

# 可视化
# 1. 基本的UMAP图
pdf("D:/Cambridge/monocle3/monocle3_umap.pdf", width = 8, height = 6)
plot_cells(cds, 
           color_cells_by = "pseudotime",
           label_cell_groups = FALSE,
           label_leaves = FALSE,
           label_branch_points = FALSE)
dev.off()

# 2. 带轨迹的UMAP图
pdf("D:/Cambridge/monocle3/monocle3_trajectory.pdf", width = 8, height = 6)
plot_cells(cds,
           color_cells_by = "pseudotime",
           label_cell_groups = FALSE,
           label_leaves = FALSE,
           label_branch_points = FALSE,
           graph_label_size = 1.5)
dev.off()

# 3. 修改后的基因表达图绘制代码
for (gene in genes_of_interest) {
  pdf(paste0("D:/Cambridge/monocle3/gene_", gene, "_pseudotime.pdf"), width = 8, height = 6)
  print(plot_genes_in_pseudotime(cds[gene,], 
                                 color_cells_by = "pseudotime"))
  dev.off()
}

# 获取pseudotime值
pseudotime_values <- pseudotime(cds)

# 创建新的整合数据框
# 1. 添加pseudotime列到原始数据
integrated_data <- expression_data
integrated_data$pseudotime <- pseudotime_values

# 2. 按pseudotime排序
integrated_data <- integrated_data[order(integrated_data$pseudotime), ]

# 3. 计算每个基因与pseudotime的相关性
correlations <- sapply(genes_of_interest, function(gene) {
  cor(integrated_data[[gene]], integrated_data$pseudotime, 
      method = "spearman", use = "complete.obs")
})

# 创建相关性数据框
correlation_df <- data.frame(
  gene = genes_of_interest,
  pseudotime_correlation = correlations
)

# 保存结果文件
# 1. 保存整合后的数据（包含所有原始数据和新添加的pseudotime）
write.csv(integrated_data, 
          "D:/Cambridge/monocle3/integrated_data_with_pseudotime.csv", 
          row.names = TRUE)

# 2. 保存基因相关性数据
write.csv(correlation_df, 
          "D:/Cambridge/monocle3/gene_pseudotime_correlations.csv", 
          row.names = FALSE)

# 输出处理结果的简要统计
cat("数据处理完成！\n")
cat("生成的文件：\n")
cat("1. integrated_data_with_pseudotime.csv - 包含", nrow(integrated_data), "行,", ncol(integrated_data), "列\n")
cat("2. gene_pseudotime_correlations.csv - 包含", nrow(correlation_df), "个基因的相关性数据\n")
cat("3. 生成了", length(genes_of_interest), "个基因的表达趋势图\n")

# 展示相关性结果
print("基因与伪时间的相关性（从高到低排序）：")
correlation_df_sorted <- correlation_df[order(-abs(correlation_df$pseudotime_correlation)), ]
print(correlation_df_sorted)

# 保存详细的分析报告
sink("D:/Cambridge/monocle3/analysis_report.txt")
cat("EMT轨迹分析报告\n")
cat("================\n\n")
cat("1. 数据概况：\n")
cat("   - 总细胞数：", nrow(integrated_data), "\n")
cat("   - 分析基因数：", length(genes_of_interest), "\n\n")
cat("2. 伪时间分析结果：\n")
cat("   - 伪时间范围：", min(pseudotime_values), "至", max(pseudotime_values), "\n\n")
cat("3. 基因相关性分析：\n")
print(correlation_df_sorted)
cat("\n4. 输出文件列表：\n")
cat("   - integrated_data_with_pseudotime.csv\n")
cat("   - gene_pseudotime_correlations.csv\n")
cat("   - monocle3_umap.pdf\n")
cat("   - monocle3_trajectory.pdf\n")
cat("   - 各基因表达趋势图\n")
sink()
