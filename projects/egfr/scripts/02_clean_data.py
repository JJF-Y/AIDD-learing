"""
第2步：数据清洗
- 去重（同一个分子多条记录取平均值）
- 只保留精确值（standard_relation == '='）
- SMILES 标准化
- 定义活性标签（pChEMBL >= 6.5 为活性）
用法：python 02_clean_data.py
"""

import pandas as pd
import os
from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize

# 文件路径
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, '..', 'data', 'egfr_raw.csv')
output_path = os.path.join(script_dir, '..', 'data', 'egfr_clean.csv')

# 活性阈值：pChEMBL >= 6.5 算活性（对应 IC50 <= 1 uM）
ACTIVE_THRESHOLD = 6.5


def standardize_smiles(smiles):
    """SMILES 标准化：统一形式"""
    if pd.isna(smiles):
        return None
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        # 标准化（去质子、电荷中和等）
        normalizer = rdMolStandardize.Normalizer()
        mol = normalizer.normalize(mol)
        # 去质子化（取最大的片段）
        lfc = rdMolStandardize.LargestFragmentChooser()
        mol = lfc.choose(mol)
        # 统一互变异构形式
        te = rdMolStandardize.TautomerEnumerator()
        mol = te.Canonicalize(mol)
        return Chem.MolToSmiles(mol)
    except Exception:
        return None


def main():
    print('=' * 50)
    print('第2步：数据清洗')
    print('=' * 50)

    # 1. 读取原始数据
    df = pd.read_csv(input_path)
    print(f'\n原始数据：{len(df)} 条')

    # 2. 去掉 SMILES 为空的
    df = df.dropna(subset=['smiles'])
    print(f'去掉空 SMILES 后：{len(df)} 条')

    # 3. 去掉 pChEMBL 为空的（没有活性数值就没用）
    df = df.dropna(subset=['pchembl_value'])
    print(f'去掉空 pChEMBL 后：{len(df)} 条')

    # 4. 只保留精确值（standard_relation == '='）
    # '>' 表示活性弱于检测下限，'<' 表示强于检测上限，都不太准
    df = df[df['standard_relation'] == '=']
    print(f'只保留精确值（=）后：{len(df)} 条')

    # 5. SMILES 标准化
    print(f'\n正在标准化 SMILES...')
    df['standard_smiles'] = df['smiles'].apply(standardize_smiles)
    df = df.dropna(subset=['standard_smiles'])
    print(f'标准化后：{len(df)} 条')

    # 6. 去重：同一个 SMILES 可能有多条记录，取 pChEMBL 平均值
    print(f'\n去重前：{len(df)} 条')
    df_agg = df.groupby('standard_smiles').agg({
        'pchembl_value': 'mean',          # 活性取平均
        'molecule_chembl_id': 'first',    # ChEMBL ID 取第一个
        'standard_type': 'first',         # 活性类型取第一个
    }).reset_index()
    print(f'去重后：{len(df_agg)} 个唯一分子')

    # 7. 定义活性标签
    df_agg['label'] = (df_agg['pchembl_value'] >= ACTIVE_THRESHOLD).astype(int)
    print(f'\n活性阈值：pChEMBL >= {ACTIVE_THRESHOLD}')
    print(f'活性（1）：{df_agg["label"].sum()} 个')
    print(f'非活性（0）：{len(df_agg) - df_agg["label"].sum()} 个')
    print(f'正负比例：{df_agg["label"].sum()} : {len(df_agg) - df_agg["label"].sum()}'
          f'  （{df_agg["label"].mean():.1%} 活性）')

    # 8. 保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_agg.to_csv(output_path, index=False)
    print(f'\n清洗后数据已保存到：{output_path}')
    print(f'共 {len(df_agg)} 个唯一分子')


if __name__ == '__main__':
    main()
