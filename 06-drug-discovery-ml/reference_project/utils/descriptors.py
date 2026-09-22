"""
分子描述符计算模块 - 参考实现
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors

DESCRIPTOR_NAMES = [
    'MolWt', 'MolLogP', 'NumHAcceptors',
    'NumHDonors', 'TPSA', 'NumRotatableBonds', 'FractionCSP3',
]

def calc_descriptors(smiles_list):
    features = []
    valid_smiles = []
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hba = Descriptors.NumHAcceptors(mol)
        hbd = Descriptors.NumHDonors(mol)
        tpsa = Descriptors.TPSA(mol)
        rot = Descriptors.NumRotatableBonds(mol)
        fsp3 = Descriptors.FractionCSP3(mol)
        features.append([mw, logp, hba, hbd, tpsa, rot, fsp3])
        valid_smiles.append(smi)
    X = np.array(features, dtype=np.float32)    
    #dtype(data type 数据类型，所以这个的作用是将数据类型转变为32位浮点数，默认是64位浮点数，两者使用上不同的是，32位占用的内存更少，相对来说机器学习时会更快，但是精确度上不如64位，但是这里用32位完全足够)
    return X, valid_smiles, DESCRIPTOR_NAMES
    #DESCRIPTOR_NAMES虽然不在函数中，但是这是在函数外的全局变量，函数可以读，但是不能改，所以函数可以输出