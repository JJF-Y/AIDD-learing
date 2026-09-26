"""
XGBoost 分子指纹回归实践
- 数据：Caco-2 细胞通透性
- 特征：Morgan 指纹 (radius=2, 2048位)
- 模型：XGBoost 回归 + RandomForest 对比
- 功能：早停、特征重要性、评估指标、可视化
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# 导入你自己写的工具函数
import sys, os
# 用脚本所在目录定位 utils，不管从哪里运行都能找到
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'utils'))
from data_loader import load_data
from fingerprints import calc_morgan_fp
from evaluation import evaluate_regression


# ===================== 第1步：加载数据 =====================
print('=' * 50)
print('第1步：加载数据')
print('=' * 50)

df = load_data('caco2_wang.csv')
print(f'列名: {df.columns.tolist()}')

# 提取 SMILES 和标签（假设标签列叫 'Y'）
smiles_list = df['Drug'].tolist() if 'Drug' in df.columns else df['SMILES'].tolist()
y = df['Y'].values

print(f'分子数: {len(smiles_list)}')
print(f'标签范围: {y.min():.2f} ~ {y.max():.2f}')
print(f'标签均值: {y.mean():.2f}')


# ===================== 第2步：计算分子指纹 =====================
print('\n' + '=' * 50)
print('第2步：计算 Morgan 指纹')
print('=' * 50)

X, valid_smiles = calc_morgan_fp(smiles_list, radius=2, n_bits=2048)

# 指纹对应的标签也要同步（有些SMILES可能解析失败被跳过了）
# 这里简单处理：假设都解析成功了，直接用全部 y
# 如果有失败的，需要重新对齐，这里先不考虑
print(f'指纹矩阵形状: {X.shape}')
print(f'指纹数据类型: {X.dtype}')
print(f'每个分子平均有 {X.sum(axis=1).mean():.0f} 个1')


# ===================== 第3步：划分数据集 =====================
print('\n' + '=' * 50)
print('第3步：划分训练集/测试集')
print('=' * 50)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f'训练集: {X_train.shape[0]} 个分子')
print(f'测试集: {X_test.shape[0]} 个分子')


# ===================== 第4步：训练 XGBoost（带早停） =====================
print('\n' + '=' * 50)
print('第4步：训练 XGBoost 回归模型')
print('=' * 50)

# 从训练集里再分一部分做验证集，用于早停
X_train_part, X_val, y_train_part, y_val = train_test_split(
    X_train, y_train, test_size=0.15, random_state=42
)

print(f'实际训练: {X_train_part.shape[0]} 个')
print(f'验证集(早停用): {X_val.shape[0]} 个')

xgb_model = XGBRegressor(
    n_estimators=1000,        # 最多1000棵树（早停会提前停）
    learning_rate=0.05,       # 学习率，小步走
    max_depth=6,              # 每棵树最大深度
    subsample=0.8,            # 每棵树随机用80%的样本
    colsample_bytree=0.8,     # 每棵树随机用80%的特征
    random_state=42,
    n_jobs=-1,                # 用所有CPU核
)

# 训练 + 早停
xgb_model.fit(
    X_train_part, y_train_part,
    eval_set=[(X_val, y_val)],   # 用验证集监控性能
    verbose=50,                  # 每50轮打印一次
)

print(f'\n实际用了 {xgb_model.best_iteration} 棵树（早停）')


# ===================== 第5步：训练 RandomForest 做对比 =====================
print('\n' + '=' * 50)
print('第5步：训练 RandomForest（对比用）')
print('=' * 50)

rf_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)
print('RandomForest 训练完成')


# ===================== 第6步：评估两个模型 =====================
print('\n' + '=' * 50)
print('第6步：模型评估')
print('=' * 50)

# XGBoost 评估
print('\n--- XGBoost (测试集) ---')
y_pred_xgb = xgb_model.predict(X_test)
result_xgb = evaluate_regression(y_test, y_pred_xgb, verbose=True)

# RandomForest 评估
print('\n--- RandomForest (测试集) ---')
y_pred_rf = rf_model.predict(X_test)
result_rf = evaluate_regression(y_test, y_pred_rf, verbose=True)

# 对比
print('\n--- 对比总结 ---')
print(f'{"指标":<8} {"XGBoost":>10} {"RandomForest":>14} {"XGB提升":>10}')
print('-' * 46)
for metric in ['r2', 'rmse', 'mae', 'mse']:
    xgb_val = result_xgb[metric]
    rf_val = result_rf[metric]
    if metric == 'r2':
        diff = xgb_val - rf_val  # R²越高越好
        sign = '+' if diff > 0 else ''
        print(f'{metric.upper():<8} {xgb_val:>10.3f} {rf_val:>14.3f} {sign}{diff:>9.3f}')
    else:
        diff = rf_val - xgb_val  # 误差越低越好
        sign = '+' if diff > 0 else ''
        print(f'{metric.upper():<8} {xgb_val:>10.3f} {rf_val:>14.3f} {sign}{diff:>9.3f}')


# ===================== 第7步：特征重要性 =====================
print('\n' + '=' * 50)
print('第7步：特征重要性 Top 20')
print('=' * 50)

importances = xgb_model.feature_importances_
top_indices = np.argsort(importances)[::-1][:20]  # 最重要的20个特征

print('排名  指纹位   重要性')
print('-' * 30)
for rank, idx in enumerate(top_indices, 1):
    print(f'{rank:>3}   第{idx:<5}位  {importances[idx]:.4f}')

# 画特征重要性图
fig, ax = plt.subplots(figsize=(10, 6))
top_names = [f'Bit {i}' for i in top_indices]
top_imp = importances[top_indices]
ax.barh(range(len(top_imp)), top_imp[::-1])
ax.set_yticks(range(len(top_imp)))
ax.set_yticklabels(top_names[::-1])
ax.set_xlabel('Importance')
ax.set_title('XGBoost 特征重要性 Top 20 (Morgan Fingerprint Bits)')
plt.tight_layout()
plt.savefig('xgb_feature_importance.png', dpi=300, bbox_inches='tight')
print('\n特征重要性图已保存: xgb_feature_importance.png')


# ===================== 第8步：预测值 vs 真实值 散点图 =====================
print('\n' + '=' * 50)
print('第8步：预测值 vs 真实值 可视化')
print('=' * 50)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# XGBoost 散点图
ax = axes[0]
ax.scatter(y_test, y_pred_xgb, alpha=0.5, s=20)
min_val = min(y_test.min(), y_pred_xgb.min())
max_val = max(y_test.max(), y_pred_xgb.max())
ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect Prediction')
ax.set_xlabel('True Value')
ax.set_ylabel('Predicted Value')
ax.set_title(f'XGBoost (R² = {result_xgb["r2"]:.3f})')
ax.legend()
ax.set_aspect('equal')

# RandomForest 散点图
ax = axes[1]
ax.scatter(y_test, y_pred_rf, alpha=0.5, s=20, color='green')
min_val = min(y_test.min(), y_pred_rf.min())
max_val = max(y_test.max(), y_pred_rf.max())
ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect Prediction')
ax.set_xlabel('True Value')
ax.set_ylabel('Predicted Value')
ax.set_title(f'RandomForest (R² = {result_rf["r2"]:.3f})')
ax.legend()
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('xgb_vs_rf_scatter.png', dpi=300, bbox_inches='tight')
print('散点图已保存: xgb_vs_rf_scatter.png')

plt.show()

print('\n' + '=' * 50)
print('全部完成！')
print('=' * 50)
