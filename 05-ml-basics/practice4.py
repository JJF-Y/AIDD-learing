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