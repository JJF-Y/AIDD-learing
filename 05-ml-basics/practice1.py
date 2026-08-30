#扩展药物数据
# 目标从头写计算特征、训练模型、输出准确率
import pubchempy as pcp

# 用药名查 SMILES
compound = pcp.get_compounds('ibuprofen', 'name')
print(f'SMILES: {compound[0].connectivity_smiles}')
print(f'分子量: {compound[0].molecular_weight}')
print(f'分子式: {compound[0].molecular_formula}')