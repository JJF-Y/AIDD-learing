#数据加载与清洗模块
import pandas as pd
from rdkit import Chem

#加载CSV数据，检查SMILES有效性，返回有效数据的DataFrame
def load_data(filepath):
    df = pd.read_csv(filepath)
    vaild_rows = []
    fail_count  = 0
    total = len(df) 
    for idx,row in df.iterrows():
        smi = str(row["SMILES"])
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            vaild_rows.append(row)
        else:
            fail_count += 1
    clean_df = pd.DataFrame(vaild_rows).reset_index(drop=True)
    print(f'数据加载完成: 共{total}条, 有效{len(clean_df)}条, 失败{fail_count}条')

c = load_data("caco2_wang.csv")