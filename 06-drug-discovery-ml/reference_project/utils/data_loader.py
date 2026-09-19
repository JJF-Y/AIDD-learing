"""
数据加载与清洗模块 - 参考实现
"""
import pandas as pd
from rdkit import Chem


def load_data(filepath):
    df = pd.read_csv(filepath)
    total = len(df)
    valid_rows = []
    fail_count = 0
    for idx, row in df.iterrows():
        smi = str(row['SMILES'])
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            valid_rows.append(row)
        else:
            fail_count += 1
    clean_df = pd.DataFrame(valid_rows).reset_index(drop=True)
    print(f'数据加载完成: 共{total}条, 有效{len(clean_df)}条, 失败{fail_count}条')
    return clean_df

j = load_data("caco2_wang.csv")
