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
        #df.iterrows() 是 pandas 的方法，逐行遍历 DataFrame，每次返回 (行号, 行数据) 这个元组。
        smi = str(row['SMILES'])#当前行的'SMILES'列的数据转变为字符串，为了避免因为pandas遇到空的填的特殊值NaN，
        # 因为这个是float浮点数，直接输入Chem.MolFromSmiles()会导致错误，但是转变为字符串就是'NaN'形式，不会报错，会返回None
        mol = Chem.MolFromSmiles(smi)
        if mol is not None:
            valid_rows.append(row)
        else:
            fail_count += 1
    clean_df = pd.DataFrame(valid_rows).reset_index(drop=True)
    print(f'数据加载完成: 共{total}条, 有效{len(clean_df)}条, 失败{fail_count}条')
    return clean_df
