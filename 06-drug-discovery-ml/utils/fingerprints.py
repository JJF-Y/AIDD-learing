"""
分子指纹计算模块
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import ConvertToNumpyArray

def calc_morgan_fp(smiles_list, radius=2, n_bits=2048):
    """计算Morgan指纹 (ECFP)"""
    pass
