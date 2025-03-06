import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

path1="data_1.6w行.csv"
path2="data_1.6w行.降维.csv"
print("开始读取文件1")
# 1. 读取数据（假设文件格式为16000行x80000列，无索引和列名）
data = pd.read_csv(path1, header=None)  # 如果文件有列名或索引，需调整参数
print("提取数值矩阵(形状应为16000x80000)")
# 2. 提取数值矩阵（形状应为16000x80000）
X = data.values  # 如果数据有表头或索引列，需用 data.iloc[:, :].values
print("标准化数据")
# 3. 标准化数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # 按列标准化（每个检测点的均值和方差）
print("PCA降维")
# 4. PCA降维
pca = PCA(n_components=256, svd_solver='randomized')
X_pca = pca.fit_transform(X_scaled)  # 输出形状为16000x256
print("转换为DataFrame并保存")
# 5. 转换为DataFrame并保存
df_pca = pd.DataFrame(X_pca)
df_pca.to_csv(path2, index=False, header=False)  # 不保存索引和列名