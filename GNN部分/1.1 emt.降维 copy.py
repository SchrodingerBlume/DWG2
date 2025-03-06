import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

path1="data_1.6w.8w.csv"
path2="data_1.6w.256.csv"
print("start read ")
data = pd.read_csv(path1, header=None) 
print("16000x80000")
X = data.values  
print("StandardScaler")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  
print("PCA")
pca = PCA(n_components=256, svd_solver='randomized')
X_pca = pca.fit_transform(X_scaled)  
print("save")
df_pca = pd.DataFrame(X_pca)
df_pca.to_csv(path2, index=False, header=False)  