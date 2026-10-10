"""
骨架划分模块 (Scaffold Split)
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem.Scaffolds.MurckoScaffold import MurckoScaffoldSmiles

def scaffold_split(smiles_list, test_size=0.2, seed=42):
    scaffolds = {}
    for idx, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        try:
            scaffold = MurckoScaffoldSmiles(mol=mol)
        except Exception:
            scaffold = 'invalid_' + str(idx)
        if scaffold not in scaffolds:
            scaffolds[scaffold] = []
        scaffolds[scaffold].append(idx)

    scaffold_list = sorted(scaffolds.items(), key=lambda x: len(x[1]), reverse=True)

    n_total = len(smiles_list)
    n_test_target = int(n_total * test_size)
    train_idx = []
    test_idx = []

    for scaffold, indices in scaffold_list:
        if len(test_idx) + len(indices) <= n_test_target:
            test_idx.extend(indices)
        else:
            train_idx.extend(indices)

    train_idx = np.array(train_idx, dtype=int)
    test_idx = np.array(test_idx, dtype=int)

    print ( f'骨架划分: 训练集 { len (train_idx)} 个, 测试集 { len (test_idx)} 个' ) 
    print ( f'骨架种类数: { len (scaffolds)} ' ) 
    return train_idx, test_idx