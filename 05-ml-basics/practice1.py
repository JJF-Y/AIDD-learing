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