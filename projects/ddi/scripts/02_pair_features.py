"""
第2步：计算分子对特征（三种策略对比）
用法：python 02_pair_features.py

三种特征策略：
1. 拼接 (concat):       [fp_A | fp_B]  → 4096维
2. 张量积 (tensor_prod): fp_A * fp_B   → 2048维（逐元素相乘）
3. 差值 (difference):    |fp_A - fp_B|  → 2048维
"""

import os
import sys
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import ConvertToNumpyArray

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
results_dir = os.path.join(script_dir, '..', 'results')


def calc_morgan_fp(smiles, radius=2, n_bits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=n_bits)
    arr = np.zeros((n_bits,), dtype=np.int8)
    ConvertToNumpyArray(fp, arr)
    return arr


def build_pair_features(df, strategy='concat', n_bits=2048):
    n_rows = len(df)
    valid_mask = []
    fps1 = []
    fps2 = []

    for idx, row in df.iterrows():
        fp1 = calc_morgan_fp(row['smiles1'], n_bits=n_bits)
        fp2 = calc_morgan_fp(row['smiles2'], n_bits=n_bits)
        if fp1 is None or fp2 is None:
            valid_mask.append(False)
            fps1.append(np.zeros(n_bits, dtype=np.int8))
            fps2.append(np.zeros(n_bits, dtype=np.int8))
        else:
            valid_mask.append(True)
            fps1.append(fp1)
            fps2.append(fp2)

        if (idx + 1) % 500 == 0:
            print(f'  处理 {idx + 1}/{n_rows}...')

    fps1 = np.array(fps1, dtype=np.int8)
    fps2 = np.array(fps2, dtype=np.int8)
    valid_mask = np.array(valid_mask)

    if strategy == 'concat':
        X = np.hstack([fps1, fps2])
    elif strategy == 'tensor_prod':
        X = fps1 * fps2
    elif strategy == 'difference':
        X = np.abs(fps1 - fps2)
    else:
        raise ValueError(f'不支持的特征策略: {strategy}')

    return X, valid_mask


def main():
    print('=' * 50)
    print('第2步：计算分子对特征')
    print('=' * 50)

    train_path = os.path.join(data_dir, 'ddi_train.csv')
    if not os.path.exists(train_path):
        print('请先运行 01_fetch_data.py')
        sys.exit(1)

    strategies = ['concat', 'tensor_prod', 'difference']

    for split_name in ['train', 'val', 'test']:
        filepath = os.path.join(data_dir, f'ddi_{split_name}.csv')
        df = pd.read_csv(filepath)
        print(f'\n{split_name} 集: {len(df)} 条')

        for strategy in strategies:
            print(f'\n  策略: {strategy}')
            X, valid_mask = build_pair_features(df, strategy=strategy)
            y = df['label'].values[valid_mask]

            np.savez(
                os.path.join(results_dir, f'{split_name}_{strategy}.npz'),
                X=X[valid_mask], y=y
            )
            print(f'    保存: {split_name}_{strategy}.npz  X={X[valid_mask].shape}  正样本比例={y.mean():.2%}')


if __name__ == '__main__':
    main()
