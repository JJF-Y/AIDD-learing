"""
第1步：获取 DDI 数据并构建二分类数据集
用法：python 01_fetch_data.py

数据来源：TDC (Therapeutics Data Commons) 的 DDI 数据集
正样本：已知有相互作用的药物对
负样本：随机采样的无相互作用药物对（1:1配比）
"""

import os
import sys
import random
import numpy as np
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')


def load_tdc_ddi():
    from tdc.multi_pred.compass.dataset import DrugDrugInteraction
    dataset = DrugDrugInteraction(name='DAVIS')
    split = dataset.get_split()
    return split


def build_binary_dataset(split, neg_ratio=1.0, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    train_df = split['train']
    val_df = split['valid']
    test_df = split['test']

    all_pos_pairs = set()
    smiles_map = {}

    for df in [train_df, val_df, test_df]:
        for _, row in df.iterrows():
            d1, d2 = row['Drug1_ID'], row['Drug2_ID']
            pair = tuple(sorted([d1, d2]))
            all_pos_pairs.add(pair)
            smiles_map[row['Drug1_ID']] = row['Drug1_SMILES']
            smiles_map[row['Drug2_ID']] = row['Drug2_SMILES']

    drug_ids = sorted(set(
        list(train_df['Drug1_ID'].unique()) +
        list(train_df['Drug2_ID'].unique())
    ))
    print(f'药物总数: {len(drug_ids)}')
    print(f'正样本对数: {len(all_pos_pairs)}')

    n_pos = len(all_pos_pairs)
    n_neg = int(n_pos * neg_ratio)

    neg_pairs = set()
    attempts = 0
    max_attempts = n_neg * 20

    while len(neg_pairs) < n_neg and attempts < max_attempts:
        d1 = random.choice(drug_ids)
        d2 = random.choice(drug_ids)
        if d1 == d2:
            attempts += 1
            continue
        pair = tuple(sorted([d1, d2]))
        if pair in all_pos_pairs or pair in neg_pairs:
            attempts += 1
            continue
        neg_pairs.add(pair)
        attempts += 1

    print(f'采样负样本: {len(neg_pairs)} (尝试 {attempts} 次)')

    pos_rows = []
    for d1, d2 in all_pos_pairs:
        pos_rows.append({
            'drug1_id': d1, 'drug2_id': d2,
            'smiles1': smiles_map.get(d1, ''), 'smiles2': smiles_map.get(d2, ''),
            'label': 1
        })

    neg_rows = []
    for d1, d2 in neg_pairs:
        neg_rows.append({
            'drug1_id': d1, 'drug2_id': d2,
            'smiles1': smiles_map.get(d1, ''), 'smiles2': smiles_map.get(d2, ''),
            'label': 0
        })

    all_rows = pos_rows + neg_rows
    random.shuffle(all_rows)
    df = pd.DataFrame(all_rows)

    n_total = len(df)
    n_train = int(n_total * 0.7)
    n_val = int(n_total * 0.15)

    train = df.iloc[:n_train].reset_index(drop=True)
    val = df.iloc[n_train:n_train + n_val].reset_index(drop=True)
    test = df.iloc[n_train + n_val:].reset_index(drop=True)

    return train, val, test


def main():
    print('=' * 50)
    print('第1步：获取 DDI 数据')
    print('=' * 50)

    try:
        from tdc import Evaluator
    except ImportError:
        print('请先安装 TDC: pip install PyTDC')
        sys.exit(1)

    print('\n正在加载 TDC DDI 数据集...')
    split = load_tdc_ddi()

    print(f'原始数据: train={len(split["train"])}, val={len(split["valid"])}, test={len(split["test"])}')

    print('\n构建二分类数据集 (1:1 正负配比)...')
    train, val, test = build_binary_dataset(split, neg_ratio=1.0, seed=42)

    print(f'\n最终数据: train={len(train)}, val={len(val)}, test={len(test)}')
    print(f'训练集正样本比例: {train["label"].mean():.2%}')

    train.to_csv(os.path.join(data_dir, 'ddi_train.csv'), index=False)
    val.to_csv(os.path.join(data_dir, 'ddi_val.csv'), index=False)
    test.to_csv(os.path.join(data_dir, 'ddi_test.csv'), index=False)

    print(f'\n数据已保存到 {data_dir}/')
    print('文件: ddi_train.csv, ddi_val.csv, ddi_test.csv')


if __name__ == '__main__':
    main()
