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
    return X, valid_smiles, DESCRIPTOR_NAMES
