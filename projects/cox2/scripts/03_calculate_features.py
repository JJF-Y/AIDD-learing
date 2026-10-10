"""
第3步：计算分子特征
- 7个基础理化描述符（MW、LogP、HBA、HBD、TPSA、RotBonds、Fsp3）
- Morgan 指纹（radius=2, n_bits=2048）
- 描述符 + 指纹 拼接成完整特征矩阵
用法：python 03_calculate_features.py
"""

import pandas as pd
import numpy as np
import os
import sys

# 把项目根目录加到路径里，方便 import utils
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(script_dir, '..')
sys.path.insert(0, project_dir)

from utils.descriptors import calc_descriptors, DESCRIPTOR_NAMES
from utils.fingerprints import calc_morgan_fp

# 文件路径
input_path = os.path.join(project_dir, 'data', 'cox2_clean.csv')
output_desc_path = os.path.join(project_dir, 'data', 'X_descriptors.npy')
output_fp_path = os.path.join(project_dir, 'data', 'X_fingerprint.npy')
output_label_path = os.path.join(project_dir, 'data', 'y_labels.npy')
output_smiles_path = os.path.join(project_dir, 'data', 'smiles_clean.npy')


def main():
    print('=' * 50)
    print('第3步：计算分子特征')
    print('=' * 50)

    # 1. 读取清洗后的数据
    df = pd.read_csv(input_path)
    print(f'\n读取数据：{len(df)} 个分子')

    smiles_list = df['standard_smiles'].tolist()
    labels = df['label'].values

    # 2. 计算理化描述符
    print(f'\n正在计算理化描述符...')
    X_desc, valid_smiles_desc, desc_names = calc_descriptors(smiles_list)
    print(f'描述符维度：{X_desc.shape[1]} 维')
    print(f'成功计算：{len(valid_smiles_desc)} 个分子')

    # 2.5 过滤异常值（去掉明显不是小分子的极端分子）
    print(f'\n正在过滤异常值...')
    # 建立描述符 DataFrame 方便筛选
    df_desc_raw = pd.DataFrame(X_desc, columns=desc_names)
    df_desc_raw.insert(0, 'smiles', valid_smiles_desc)

    # 过滤条件：针对 Cox-2 小分子抑制剂的合理范围
    filter_mask = (
        (df_desc_raw['MolWt'] < 1000) &        # 分子量小于 1000（排除多肽/大环等）
        (df_desc_raw['NumRotatableBonds'] < 20) # 可旋转键少于 20（排除长链分子）
    )

    n_before = len(df_desc_raw)
    df_desc_filtered = df_desc_raw[filter_mask].reset_index(drop=True)
    n_after = len(df_desc_filtered)
    n_removed = n_before - n_after

    print(f'过滤前：{n_before} 个分子')
    print(f'过滤掉：{n_removed} 个分子（{n_removed/n_before*100:.1f}%）')
    print(f'过滤条件：MolWt < 1000 且 NumRotatableBonds < 20')

    # 更新描述符矩阵和 SMILES 列表
    X_desc = df_desc_filtered[desc_names].values
    filtered_smiles = df_desc_filtered['smiles'].tolist()

    # 3. 计算 Morgan 指纹（只算过滤后的分子，省时间）
    print(f'\n正在计算 Morgan 指纹 (radius=2, n_bits=2048)...')
    X_fp, valid_smiles_fp = calc_morgan_fp(filtered_smiles, radius=2, n_bits=2048)
    print(f'指纹维度：{X_fp.shape[1]} 维')
    print(f'成功计算：{len(valid_smiles_fp)} 个分子')

    # 4. 对齐：确保描述符和指纹的分子顺序一致
    # （两套特征都用 filtered_smiles，顺序应该一致，这里做一下检查）
    assert len(valid_smiles_fp) == len(filtered_smiles), \
        f'指纹计算失败：预期 {len(filtered_smiles)} 个，实际 {len(valid_smiles_fp)} 个'

    # 从原始标签中取出过滤后分子对应的标签
    # 建立 SMILES → label 的映射
    smiles_to_label = dict(zip(smiles_list, labels))
    y = np.array([smiles_to_label[smi] for smi in filtered_smiles])
    valid_smiles_arr = np.array(filtered_smiles)

    print(f'\n最终有效分子：{len(y)} 个')
    print(f'活性（1）：{y.sum()} 个')
    print(f'非活性（0）：{len(y) - y.sum()} 个')

    # 5. 保存为 numpy 格式（模型训练直接读，快）
    np.save(output_desc_path, X_desc)
    np.save(output_fp_path, X_fp)
    np.save(output_label_path, y)
    np.save(output_smiles_path, valid_smiles_arr)

    print(f'\n特征已保存：')
    print(f'  描述符：{output_desc_path}  {X_desc.shape}')
    print(f'  指纹：  {output_fp_path}  {X_fp.shape}')
    print(f'  标签：  {output_label_path}  {y.shape}')
    print(f'  SMILES：{output_smiles_path}  {valid_smiles_arr.shape}')

    # 6. 顺便保存描述符为 CSV（方便查看）
    df_desc = pd.DataFrame(X_desc, columns=desc_names)
    df_desc.insert(0, 'smiles', filtered_smiles)
    df_desc['label'] = y
    desc_csv_path = os.path.join(project_dir, 'data', 'descriptors.csv')
    df_desc.to_csv(desc_csv_path, index=False)
    print(f'\n描述符 CSV（方便查看）：{desc_csv_path}')


if __name__ == '__main__':
    main()
