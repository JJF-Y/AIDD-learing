#用别的模型去训练并预测
#导入模块
import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_squared_error, r2_score)

from rdkit import Chem
from rdkit.Chem import Descriptors

import pubchempy as pcp

items = [
    'loratadine',      # 氯雷他定（抗过敏）
    'fexofenadine',    # 非索非那定（抗过敏）
    'cetirizine',      # 西替利嗪（抗过敏）
    'pantoprazole',    # 泮托拉唑（抑酸）
    'lansoprazole',    # 兰索拉唑（抑酸）
    'rosuvastatin',    # 瑞舒伐他汀（降脂）
    'pravastatin',     # 普伐他汀（降脂）
    'losartan',        # 氯沙坦（降压）
    'amlodipine',      # 氨氯地平（降压）
    'metoprolol',      # 美托洛尔（降压）
    'levofloxacin',    # 左氧氟沙星（抗生素）
    'clarithromycin',  # 克拉霉素（抗生素，偏大）
    'fluoxetine',      # 氟西汀（抗抑郁）
    'sertraline',      # 舍曲林（抗抑郁）
    'olanzapine',      # 奥氮平（抗精神病）
    'cyclosporine',    # 环孢素（大分子）
    'tacrolimus',      # 他克莫司（大分子，免疫抑制剂）
    'sirolimus',       # 西罗莫司（大分子）
    'doxorubicin',     # 多柔比星（抗肿瘤，偏大）
    'paclitaxel',      # 紫杉醇（抗肿瘤，大分子）
]

compounds = []
smiles = []
names = []
drug_smiles = []
features = []

for name in items:
    c = pcp.get_compounds(name,'name')
    names.append(name)
    if c:
        smile = c[0].connectivity_smiles
        smiles.append(smile)

drug_smiles = dict(zip(names,smiles))

for name , smile in drug_smiles.items():
    mol = Chem.MolFromSmiles(smile)
    if mol == None:
        print('失败')
        continue
    mw  = Descriptors.MolWt(mol)
    logP = Descriptors.MolLogP(mol)
    hba  = Descriptors.NumHAcceptors(mol)
    hbd = Descriptors.NumHDonors(mol)
    features.append([mw, logP, hba, hbd])
    names.append(name)