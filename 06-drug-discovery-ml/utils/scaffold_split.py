"""
骨架划分模块 (Scaffold Split)
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem.Scaffolds.MurckoScaffold import MurckoScaffoldSmiles

def scaffold_split(smiles_list, test_size=0.2, seed=42):
    """按Murcko骨架划分训练集和测试集"""
    pass
