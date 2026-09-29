"""
分子指纹计算模块
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import ConvertToNumpyArray

def calc_morgan_fp(smiles_list, radius=2, n_bits=2048):
    fps = []
    valid_smiles = []

    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is  None:
            continue
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=n_bits)
        arr = np.zeros((n_bits,), dtype=np.int8)
        ConvertToNumpyArray(fp, arr)
        fps.append(arr)
        valid_smiles.append(smi)

    X = np.array(fps, dtype=np.int8)
    return X, valid_smiles