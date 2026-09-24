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
        #AllChem是RDKit的化学功能模块，GetMorganFingerprint是获取 Morgan 指纹，AsBitVect是 A s B it Vect or，以位向量形式返回,radius=radius指纹半径，nBits=n_bits指纹总位数
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

#检验
if __name__ == '__main__' :
    test_smiles = [
        'CC(=O)Oc1ccccc1C(=O)O' ,
        'CC(=O)Nc1ccc(O)cc1' ,
        'CC(C)Cc1ccc(cc1)C(C)C(=O)O' ,
        'CN1C=NC2=C1C(=O)N(C(=O)N2C)C' ,
        'C1CCCCC1无效' ,
    ]
    X, valid = calc_morgan_fp(test_smiles)
    print ( f'矩阵形状: {X.shape} ' )
    print ( f'有效分子数: { len (valid)} ' ) 
    assert X.shape == ( 4 , 2048 ), f'形状不对: {X.shape} ' 
    assert len (valid) == 4 , f'有效分子数不对: { len (valid)} ' 
    print ( '✓ 形状检验通过' )

    print ( f'数据类型: {X.dtype} ' ) 
    assert X.dtype == np.int8, f'类型不对: {X.dtype} ' 
    print ( '✓ 数据类型检验通过' )

    unique_vals = np.unique(X) 
    print ( f'出现的值: {unique_vals} ' ) 
    assert set (unique_vals).issubset({ 0 , 1 }), '指纹不只有0和1' 
    print ( '✓ 0/1值检验通过' )

    ones_count = X. sum (axis= 1 ) 
    print ( f'每个分子1的个数: {ones_count} ' ) 
    assert all (c > 0 for c in ones_count), '有分子全是0' 
    print ( '✓ 非零检验通过' )

    fp_aspirin = X[ 0 ]
    fp_paracetamol = X[ 1 ]
    similarity = np. sum (fp_aspirin & fp_paracetamol) / np. sum (fp_aspirin | fp_paracetamol) 
    print ( f'阿司匹林 vs 对乙酰氨基酚 相似度: {similarity: .3 f} ' ) 
    assert not np.array_equal(fp_aspirin, fp_paracetamol), '两个不同分子指纹居然一样' 
    print ( '✓ 差异性检验通过' )

    X2, _ = calc_morgan_fp([ 'CC(=O)Oc1ccccc1C(=O)O' ]) 
    assert np.array_equal(X[ 0 ], X2[ 0 ]), '相同分子指纹不一样' 
    print ( '✓ 一致性检验通过' ) 
    print ( '\n========== 全部检验通过！ ==========' )
