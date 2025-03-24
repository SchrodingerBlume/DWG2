import pandas as pd
import numpy as np
from tqdm import tqdm

# File paths
input_file = 'filtered_normalized_expression.csv'
output_file = 'EMT_score_result.csv'

# Target genes
target_genes = {'CDH1', 'VIM', 'CLDN7'}
gene_data = {}

print("Reading the file line by line to filter target genes...")

with open(input_file, 'r') as f:
    header = f.readline().strip().split(',')  # The first line contains sample names
    for line in tqdm(f, desc="Scanning genes"):
        parts = line.strip().split(',')
        gene = parts[0].strip().strip('"').strip("'")
        if gene in target_genes:
            gene_data[gene] = np.array(parts[1:], dtype=np.float64)
        if len(gene_data) == len(target_genes):
            break

missing = target_genes - gene_data.keys()
if missing:
    print(f"Warning: The following genes are missing: {missing}")

print("Calculating log2 transformation of expressions...")

cdh1 = gene_data.get('CDH1', np.full(len(header)-1, np.nan))
vim = gene_data.get('VIM', np.full(len(header)-1, np.nan))
cldn7 = gene_data.get('CLDN7', np.full(len(header)-1, np.nan))

# Compute the log2 expression ratio
log2_vim = np.log2(np.where(vim > 0, vim, np.nan))
log2_cdh1 = np.log2(np.where(cdh1 > 0, cdh1, np.nan))
log2_vim_div_log2_cdh1 = np.divide(
    log2_vim,
    log2_cdh1,
    out=np.full_like(log2_vim, np.nan),
    where=~np.isnan(log2_cdh1)
)
log2_cldn7 = np.log2(np.where(cldn7 > 0, cldn7, np.nan))

# Construct the DataFrame
df = pd.DataFrame({
    'Sample': header[1:],
    'CDH1': cdh1,
    'VIM': vim,
    'CLDN7': cldn7,
    'log2_VIM_div_log2_CDH1': log2_vim_div_log2_cdh1,
    'log2_CLDN7': log2_cldn7,
})

# Remove rows that contain 0 expression
df = df[
    ~((df['CDH1'] == 0) |
      (df['VIM'] == 0) |
      (df['CLDN7'] == 0))
].copy()

# ================== Calculate EMT μ ==================
alpha1 = -7.87
alpha2 = 0.0413
beta1 = 1.36
beta2 = -1.96

def compute_mu(x1, x2):
    z = beta1 * x1 + beta2 * x2
    pe = np.exp(alpha1 - z) / (1 + np.exp(alpha1 - z))
    pem = np.exp(alpha2 - z) / (1 + np.exp(alpha2 - z)) - pe
    pm = 1 - pe - pem
    mu = 0 * pe + 1 * pem + 2 * pm
    return mu

tqdm.pandas(desc="Calculating EMT μ")
df['mu'] = df.progress_apply(
    lambda row: compute_mu(
        row['log2_VIM_div_log2_CDH1'],
        row['log2_CLDN7']
    ),
    axis=1
)

# Save the results
df.to_csv(output_file, index=False, float_format='%.10e')
print(f"All steps have been completed. The final results have been saved in: {output_file}")