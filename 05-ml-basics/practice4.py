#完整的一个，从数据加载到模型训练和评估，以及数据的可视化

#先简单捋一下思路，先获取药名，再根据药名获取药物的相关信息，然后进行数据清洗和预处理，最后进行模型训练和评估。同时尝试优化原有的思路

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_squared_error, r2_score)

from rdkit import Chem
from rdkit.Chem import Descriptors

import pubchempy as pcp

import time

import csv

import os

import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
from drug_names_500 import drug_names
from test_drugs_500 import test_drugs

#为了避免每次测试都要重新获取，所以第一次获取后保存到本地，之后直接读取本地文件即可
#那么可以先做关于药物SMILES的获取的函数封装，然后再将运行结果进行本地保存

def get_drug_smiles(name_list, filename='drug_smiles.csv'):
    
    drug_smiles = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                drug_smiles[row[0]] = row[1]
    
    todo = [name for name in name_list if name not in drug_smiles]

    if not todo:
        print('全部已查询，直接读取缓存')
        return drug_smiles 
    print(f'已有 {len(drug_smiles)} 个，还需查询 {len(todo)} 个')

    for name in todo:
        for attempt in range(3):
            try:
                c = pcp.get_compounds(name, 'name')
                if c:
                    drug_smiles[name] = c[0].connectivity_smiles
                break
            except Exception:
                time.sleep(1)
                continue
        else:
            print(f'{name} 查询失败，跳过')
        time.sleep(0.3)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'SMILES'])
        for name, smiles in drug_smiles.items():
            writer.writerow([name, smiles])
    
    return drug_smiles

def calc_descriptors(drug_smiles):
    features = []
    labels = []
    violations_list = []
    for name,smiles in drug_smiles.items():
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f'{name} 解析失败')
            continue

        mw= Descriptors.MolWt(mol)
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
        violations_list.append(violations)
        labels.append(1 if violations <= 1 else 0)

    X = np.array(features)
    y = np.array(labels)
    return X,y,violations_list

def model_fit_regression(X,y_reg):
    X_train, X_test, y_train, y_test = train_test_split(X, y_reg, test_size=0.3, random_state=42)

    model_reg = RandomForestRegressor(n_estimators=200, random_state=42)
    model_reg.fit(X_train, y_train)

    y_pred_reg = model_reg.predict(X_test)

    mse = mean_squared_error(y_test, y_pred_reg)
    r2 = r2_score(y_test, y_pred_reg)

    print(f"回归模型MSE: {mse:.2f}")
    print(f"回归模型R²: {r2:.2f}")

    return model_reg

def model_fit_Classifier(X,y,feature_names):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)

    scores = cross_val_score(model, X_train, y_train, cv=10)
    print(f'交叉验证准确率: {scores.mean():.2f} ± {scores.std():.2f}')

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f'准确率: {accuracy_score(y_test, y_pred):.2f}')

    importances = model.feature_importances_
    print("特征重要性:")
    for i, importance1 in enumerate(importances):
        print(f"  {feature_names[i]}: {importance1:.3f}")
    return model,X_test,y_test,y_pred,importances

def evaluate_model(model, X_test, y_test, y_pred,test_drugs):
    cm = confusion_matrix(y_test, y_pred)
    print('混淆矩阵:')
    print(cm)
    print(classification_report(y_test, y_pred, target_names=['不合格', '合格']))
    return cm

def plot_feature_importance(importances, feature_names):
    indices = np.argsort(importances)[::-1]
    sorted_names = [feature_names[i] for i in indices]
    sorted_importances = importances[indices]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(range(len(sorted_importances)), sorted_importances)
    ax.set_xticks(range(len(sorted_names)))
    ax.set_xticklabels(sorted_names, rotation=45, ha='right')
    ax.set_ylabel('Imoprtance')
    ax.set_title('Feature Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)
    plt.show()

drug_smiles = get_drug_smiles(drug_names)

X,y ,violations= calc_descriptors(drug_smiles)

feature_names = ['MW', 'LogP', 'HBA', 'HBD', 'TPSA', 'RotatableBonds', 'Fsp3']

model, X_text, y_text, y_pred, importance_Classifier = model_fit_Classifier(X, y, feature_names)

from test_drugs_500 import test_drugs
test_smiles = get_drug_smiles(test_drugs,"text_drug_smiles.csv")

X_new, y_new, new_violations= calc_descriptors(test_smiles)
predictions = model.predict(X_new)

model_regressor = model_fit_regression(X, violations)

text = plot_feature_importance(importance_Classifier,feature_names)