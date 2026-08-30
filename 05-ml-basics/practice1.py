#扩展药物数据
# 目标从头写计算特征、训练模型、输出准确率

#导入模块
import numpy as np  #数据处理
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_squared_error, r2_score)

from rdkit import Chem
from rdkit.Chem import Descriptors

import pubchempy as pcp

#数据
drug_names = [
    'aspirin',        # 阿司匹林
    'caffeine',       # 咖啡因
    'paracetamol',    # 对乙酰氨基酚
    'ibuprofen',      # 布洛芬
    'naproxen',       # 萘普生
    'metformin',      # 二甲双胍
    'warfarin',       # 华法林
    'diclofenac',     # 双氯芬酸
    'omeprazole',     # 奥美拉唑
    'simvastatin',    # 辛伐他汀
    'atorvastatin',   # 阿托伐他汀
    'cyclosporine',   # 环孢素（大分子，肽类）
    'vancomycin',     # 万古霉素（大分子，糖肽类）
    'erythromycin',   # 红霉素（大分子，大环内酯）
    'digoxin',        # 地高辛（大分子，强心苷）
]
#创建三个空列表，先处理数据
features = []
lables = []
names = []
drug_smiles = []
smiles = []

#不对，没有smile式，先获取
compounds = []
for name in drug_names:
    c = pcp.get_compounds(name, 'name')
    if c:
       smile = c[0].connectivity_smiles
       smiles.append(smile)
drug_smiles = dict(zip(drug_names,smiles))


#先拆包，把数据拿出来,循环的话是一个一个进行的
for name,smiles in drug_smiles.items():
    mol = Chem.MolFromSmiles(smile) #转成分子对象
    if mol is None:
        print("失败")
        continue
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hba = Descriptors.NumHAcceptors(mol)
    hbd = Descriptors.NumHDonors(mol)
    features .append([mw,logp,hba,hbd])
    names.append(name)
    violation = 0
    if mw > 500 : violation += 1
    if logp >  5 : violation += 1
    if hba  > 10 : violation += 1
    if hbd >  5 : violation += 1
    lables.append(1 if violation <= 1 else 0)

