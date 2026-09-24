"""
分子指纹计算模块 - 参考实现
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import ConvertToNumpyArray

def calc_morgan_fp(smiles_list, radius=2, n_bits=2048):
    #参数分别是SMILES字符串列表，randius指纹半径，n_bits=2048指纹长度
    fps = []    #fingerprint指纹
    valid_smiles = []   #有效的SMILES
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        #AllChem是RDKit的化学功能模块，GetMorganFingerprint是获取 Morgan 指纹，AsBitVect是 A s B it Vect or，以位向量形式返回
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=n_bits)
        #np.zeros((n_bits,))创建全0数组，长度2048.dtype=np.int8用8位整数(0或1，省空间)
        arr = np.zeros((n_bits,), dtype=np.int8)
        #把 RDKit 指纹对象转成 NumPy 数组，因为RDKit的指纹是自己的格式(ExplicitBitVect),并不能用于机器学习
        ConvertToNumpyArray(fp, arr)
        fps.append(arr)
        valid_smiles.append(smi)
    #组装成矩阵
    X = np.array(fps, dtype=np.int8)
    return X, valid_smiles
