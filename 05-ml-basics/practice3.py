#测别的特征
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
import time



items = [
    # 心血管（1-20）
    'enalapril',          'lisinopril',         'perindopril',
    'telmisartan',        'valsartan',          'irbesartan',
    'bisoprolol',         'carvedilol',         'atenolol',
    'nadolol',            'pindolol',           'nifedipine',
    'felodipine',         'nicardipine',        'nimodipine',
    'verapamil',          'diltiazem',          'doxazosin',
    'tamsulosin',         'terazosin',
    # 抗菌（21-40）
    'cephalexin',         'cefaclor',           'cefixime',
    'sulfamethoxazole',   'trimethoprim',       'nitrofurantoin',
    'metronidazole',      'tinidazole',         'chloramphenicol',
    'clindamycin',        'tetracycline',       'doxycycline',
    'minocycline',        'ciprofloxacin',      'norfloxacin',
    'ofloxacin',          'moxifloxacin',
    # 抗炎镇痛（41-48）
    'indomethacin',       'sulindac',           'ketoprofen',
    'flurbiprofen',       'piroxicam',          'meloxicam',
    'celecoxib',          'etodolac',
    # 镇痛中枢（49-68）
    'nabumetone',         'ketorolac',          'tramadol',
    'buprenorphine',      'methadone',          'naloxone',
    'levodopa',           'carbidopa',          'amantadine',
    'memantine',          'rivastigmine',       'donepezil',
    'topiramate',         'lamotrigine',        'gabapentin',
    'pregabalin',         'ethosuximide',       'primidone',
    'levetiracetam',      'alprazolam',
    # 精神消化内分泌（69-80）
    'midazolam',          'zolpidem',           'zopiclone',
    'buspirone',          'famotidine',         'nizatidine',
    'misoprostol',        'metoclopramide',     'ondansetron',
    'loperamide',         'pioglitazone',       'rosiglitazone',
    # 大分子（81-100）
    'tobramycin',         'kanamycin',          'amphotericin',
    'capreomycin',        'bacitracin',         'teicoplanin',
    'daptomycin',         'caspofungin',        'micafungin',
    'anidulafungin',      'midecamycin',        'spiramycin',
    'josamycin',          'roxithromycin',      'telithromycin',
    'fidaxomicin',        'rifabutin',          'viomycin',
    'nystatin',           'natamycin',
]

names = []
smiles = []
features = []
labels = []

for name in items:  #遍历
    for attempt in range(3):    #每个最多尝试3次
        try:    #尝试，避免因为出错导致后续代码无法进行，所以可以把可能出错的代码放在try里面，相当于隔离，出错了就跳到expect里面去处理,这两个是配对的
            c = pcp.get_compounds(name, 'name')
            if c:
                smiles.append(c[0].connectivity_smiles)
                names.append(name)
            break   #如果成功了就打破循环，没成功就继续尝试
        except Exception:   #看try情况，如果失败就转到这里，避免出错
            time.sleep(1)
            continue    #处理完出错后返回，下一个
    else:   #for... else，只有前面正常运行时，才会执行else，前面break了就不会执行
        print(f'{name} 查询失败，跳过')
    time.sleep(0.3)

drug_smiles = dict(zip(names, smiles))

for name , smiles in drug_smiles.items():
    mol = Chem.MolFromSmiles(smiles)
    if mol == None:
        print('失败')
        continue
    mw   = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hba  = Descriptors.NumHAcceptors(mol)
    hbd  = Descriptors.NumHDonors(mol)
    tpsa = Descriptors.TPSA(mol)
    rotatable = Descriptors.NumRotatableBonds(mol)
    fsp3 = Descriptors.FractionCSP3(mol)
    features.append([mw, logp, hba, hbd, tpsa, rotatable, fsp3])
    violations = 0
    if mw > 500:
        violations += 1
    if logp > 5:
        violations += 1
    if hba > 10:
        violations += 1
    if hbd > 5:
        violations += 1
    if tpsa > 140:
        violations += 1
    if rotatable > 10:
        violations += 1
    if fsp3 < 0.47:
        violations += 1
    labels.append(1 if violations <= 1 else 0) 

X = np.array(features)
y = np.array(labels)

feature_names = ['MW', 'LogP', 'HBA', 'HBD', 'TPSA', 'RotatableBonds', 'Fsp3']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model1 = RandomForestClassifier(n_estimators=100, random_state=42)
score = cross_val_score(model1, X_train, y_train, cv=10)
print(f'交叉验证准确率: {score.mean():.2f} ± {score.std():.2f}')

model1.fit(X_train, y_train)
y_pred1 = model1.predict(X_test)
print(f'准确率: {accuracy_score(y_test, y_pred1):.2f}')
importances1 = model1.feature_importances_
print("特征重要性:")
for i, importance1 in enumerate(importances1):
    print(f"  {feature_names[i]}: {importance1:.3f}")

model2 = RandomForestRegressor(n_estimators=100, random_state=42)
model2.fit(X_train, y_train)
y_pred2 = model2.predict(X_test)
print(f'回归准确率: {r2_score(y_test, y_pred2):.2f}')
print("特征重要性:")
importances2 = model2.feature_importances_
for i, importance2 in enumerate(importances2):
    print(f"  {feature_names[i]}: {importance2:.3f}")