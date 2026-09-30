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
from rdkit.Chem.MolStandardize import rdMolStandardize  #RDKit 的分子标准化工具，最重要的

# 文件路径
#__file__当前脚本文件的路径，os.path.abspath(__file__)转成绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, '..', 'data', 'egfr_raw.csv')
output_path = os.path.join(script_dir, '..', 'data', 'egfr_clean.csv')

# 活性阈值：pChEMBL >= 6.5 算活性（对应 IC50 <= 1 uM）
ACTIVE_THRESHOLD = 6.5

#SMILES标准化函数
def standardize_smiles(smiles):
    """SMILES 标准化：统一形式"""
    #pd.isna()用来判断一个值是不是空的(NaN、NaT、None 都算)
    if pd.isna(smiles):
        return None
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        # 标准化（去质子、电荷中和等）
        #第一步归一化，处理电荷,官能团的表达方式，统一成一种写法
        normalizer = rdMolStandardize.Normalizer()  #创建一个 Normalizer 对象。用它来处理分子
        mol = normalizer.normalize(mol)
        # 去盐（取最大的片段）
        #创建一个 LargestFragmentChooser 对象（最大片段选择器）
        lfc = rdMolStandardize.LargestFragmentChooser()
        #.choose(mol)从分子中选出最大的那个片段，返回新的 Mol 对象。
        mol = lfc.choose(mol)
        # 统一互变异构形式
        #创建一个 TautomerEnumerator 对象（互变异构枚举器）。
        te = rdMolStandardize.TautomerEnumerator()
        mol = te.Canonicalize(mol)
        #输出是标准化后的SMILES,或者None
        #Chem.MolToSmiles(mol)：MolFromSmiles 的逆操作——从分子对象生成 SMILES 字符串。
        return Chem.MolToSmiles(mol)
    except Exception:
        return None

# main()函数是脚本的主入口。开头打印分隔线和标题，让输出看起来清楚。
def main():
    print('=' * 50)
    print('第2步：数据清洗')
    print('=' * 50)

    # 1. 读取原始数据
    df = pd.read_csv(input_path)
    print(f'\n原始数据：{len(df)} 条')

    # 2. 去掉 SMILES 为空的
    #subset=['smiles']的意思是：只看smiles这一列，这一列空才删。
    df = df.dropna(subset=['smiles'])
    print(f'去掉空 SMILES 后：{len(df)} 条')

    # 3. 去掉 pChEMBL 为空的（没有活性数值就没用）
    df = df.dropna(subset=['pchembl_value'])
    print(f'去掉空 pChEMBL 后：{len(df)} 条')

    # 4. 只保留精确值（standard_relation == '='）
    # '>' 表示活性弱于检测下限，'<' 表示强于检测上限，都不太准
    #`df['standard_relation'] == '='` 会生成一个布尔序列（True/False），然后用这个序列去筛选行——只保留为 True 的行。
    df = df[df['standard_relation'] == '=']
    print(f'只保留精确值（=）后：{len(df)} 条')

    # 5. SMILES 标准化
    print(f'\n正在标准化 SMILES...')
    #apply()作用是对Series中的每个元素都调用一次指定的函数
    df['standard_smiles'] = df['smiles'].apply(standardize_smiles)
    #df = df.dropna(subset=['standard_smiles'])：删掉标准化失败的行（函数返回 None 的那些）。
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
    #.astype(int)把布尔值转成整数，True变1，None变0
    df_agg['label'] = (df_agg['pchembl_value'] >= ACTIVE_THRESHOLD).astype(int)
    print(f'\n活性阈值：pChEMBL >= {ACTIVE_THRESHOLD}')
    print(f'活性（1）：{df_agg["label"].sum()} 个')
    print(f'非活性（0）：{len(df_agg) - df_agg["label"].sum()} 个')
    print(f'正负比例：{df_agg["label"].sum()} : {len(df_agg) - df_agg["label"].sum()}'
          f'  （{df_agg["label"].mean():.1%} 活性）')

    # 8. 保存
    #确保输出目录存在。os.path.dirname(output_path)：取 output_path 的目录部分。exist_ok=True意思是"目录已经存在也不报错"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_agg.to_csv(output_path, index=False)
    print(f'\n清洗后数据已保存到：{output_path}')
    print(f'共 {len(df_agg)} 个唯一分子')


if __name__ == '__main__':
    main()
