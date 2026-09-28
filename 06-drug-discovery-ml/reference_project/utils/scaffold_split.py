"""
骨架划分模块 (Scaffold Split) - 参考实现
"""
import numpy as np
from rdkit import Chem
from rdkit.Chem.Scaffolds.MurckoScaffold import MurckoScaffoldSmiles


def scaffold_split(smiles_list, test_size=0.2, seed=42):
    # 1. 计算每个分子的骨架
    scaffolds = {}
    #enumerate循环给序号
    for idx, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        try:    #尝试算这个分子的骨架
            scaffold = MurckoScaffoldSmiles(mol=mol)
        except Exception:   #如果算骨架失败了，给个标记名
            scaffold = 'invalid_' + str(idx)
        #作用相当于把相同骨架的分子归类，形式类似于一种骨架，[分子序号]形成一个字典
        #如果这个骨架第一次出现，在字典里给它开个空列表
        if scaffold not in scaffolds:
            scaffolds[scaffold] = []
        #把这个分子的下标塞进对应骨架的列表里
        scaffolds[scaffold].append(idx)

    # 2. 按骨架大小从大到小排序
    #scaffolds.items()：把字典变成 (骨架, 索引列表) 的元组列表，key=lambda x: len(x[1])按每个骨架组里的分子数量排序，reverse=True从大到小
    scaffold_list = sorted(scaffolds.items(), key=lambda x: len(x[1]), reverse=True)

    # 3. 逐个分配骨架，大骨架优先放训练集，大骨架组分子数多
    n_total = len(smiles_list)
    n_test_target = int(n_total * test_size)
    train_idx = []
    test_idx = []

    #一遍一遍的加给测试集，从大到小，直到超标，然后加给训练集，如此循环直至骨架分完
    for scaffold, indices in scaffold_list:
        if len(test_idx) + len(indices) <= n_test_target:
            test_idx.extend(indices)
        else:
            train_idx.extend(indices)

    #转成 numpy 数组方便后面用索引取数据
    train_idx = np.array(train_idx, dtype=int)
    test_idx = np.array(test_idx, dtype=int)

    print ( f'骨架划分: 训练集 { len (train_idx)} 个, 测试集 { len (test_idx)} 个' ) 
    print ( f'骨架种类数: { len (scaffolds)} ' ) 
    return train_idx, test_idx