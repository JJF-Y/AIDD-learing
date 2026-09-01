#用别的模型去训练并预测
#导入模块
import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
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
    'codeine',            # 可待因
    'morphine',           # 吗啡
    'lidocaine',          # 利多卡因
    'ranitidine',         # 雷尼替丁
    'domperidone',        # 多潘立酮
    'carbamazepine',      # 卡马西平
    'phenytoin',          # 苯妥英
    'chlorpromazine',     # 氯丙嗪
    'haloperidol',        # 氟哌啶醇
    'hydrochlorothiazide',# 氢氯噻嗪
    'furosemide',         # 呋塞米
    'spironolactone',     # 螺内酯
    'glipizide',          # 格列吡嗪
    'cimetidine',         # 西咪替丁
    'allopurinol',        # 别嘌醇
    'theophylline',       # 茶碱
    'prednisolone',       # 泼尼松龙
    'dexamethasone',      # 地塞米松
    'hydrocortisone',     # 氢化可的松
    'betamethasone',      # 倍他米松
    'budesonide',         # 布地奈德
    'terbutaline',        # 特布他林
    'salbutamol',         # 沙丁胺醇
    'mirtazapine',        # 米氮平
    'venlafaxine',        # 文拉法辛
    'bleomycin',          # 博来霉素（大分子）
    'gentamicin',         # 庆大霉素（大分子）
    'amikacin',           # 阿米卡星（大分子）
    'streptomycin',       # 链霉素（大分子）
    'neomycin',           # 新霉素（大分子）
]

compounds = []
smiles = []
names = []
drug_smiles = []
features = []
labels = []

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
    violations = 0
    if mw > 500:
        violations += 1
    if logP > 5:
        violations += 1
    if hba > 10:
        violations += 1
    if hbd > 5:
        violations += 1
    labels.append(1 if violations <= 1 else 0)
print(labels)

X = np.array(features)
y = np.array(labels)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42,stratify=y)

model1 = LogisticRegression(max_iter=200, random_state=42)
model1.fit(x_train, y_train)
y_pred = model1.predict(x_test) 
print(f'准确率: {accuracy_score(y_test, y_pred):.2f}')

model2 = RandomForestClassifier(n_estimators=200, random_state=42)
model2.fit(x_train, y_train)
y_pred2 = model2.predict(x_test)
print(f'准确率: {accuracy_score(y_test, y_pred2):.2f}')

cv1 = cross_val_score(model1, X, y, cv=5)
cv2 = cross_val_score(model2, X, y, cv=5)
print(f'逻辑回归: {cv1.mean():.2f} ± {cv1.std():.2f}')
print(f'随机森林: {cv2.mean():.2f} ± {cv2.std():.2f}')