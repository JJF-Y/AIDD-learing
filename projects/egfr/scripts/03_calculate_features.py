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
input_path = os.path.join(project_dir, 'data', 'egfr_clean.csv')
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

    # 3. 计算 Morgan 指纹
    print(f'\n正在计算 Morgan 指纹 (radius=2, n_bits=2048)...')
    X_fp, valid_smiles_fp = calc_morgan_fp(smiles_list, radius=2, n_bits=2048)
    print(f'指纹维度：{X_fp.shape[1]} 维')
    print(f'成功计算：{len(valid_smiles_fp)} 个分子')

    # 4. 对齐：确保描述符和指纹的分子顺序一致
    # （两套特征都用相同的 SMILES 列表，顺序应该是一致的）
    assert len(valid_smiles_desc) == len(valid_smiles_fp), \
        f'描述符和指纹的有效分子数不一致：{len(valid_smiles_desc)} vs {len(valid_smiles_fp)}'

    # 取出对齐后的标签（用描述符那边的 valid_smiles 做基准）
    valid_indices = [i for i, smi in enumerate(smiles_list) if smi in set(valid_smiles_desc)]
    y = labels[valid_indices]
    valid_smiles_arr = np.array(valid_smiles_desc)

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
    df_desc.insert(0, 'smiles', valid_smiles_desc)
    df_desc['label'] = y
    desc_csv_path = os.path.join(project_dir, 'data', 'descriptors.csv')
    df_desc.to_csv(desc_csv_path, index=False)
    print(f'\n描述符 CSV（方便查看）：{desc_csv_path}')


if __name__ == '__main__':
    main()
