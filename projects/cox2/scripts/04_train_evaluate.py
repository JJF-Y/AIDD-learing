"""
第4步：模型训练与评估
- 特征：描述符、指纹、描述符+指纹 三种特征对比
- 模型：RandomForest、XGBoost、SVM 三种模型对比
- 划分：随机划分 + 骨架划分 两种验证方式
- 评估：准确率、精确率、召回率、F1、AUC-ROC、混淆矩阵
用法：python 04_train_evaluate.py
"""

import numpy as np
import os
import sys
import time

# 把项目根目录加到路径里
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(script_dir, '..')
sys.path.insert(0, project_dir)

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from utils.scaffold_split import scaffold_split

# 文件路径
data_dir = os.path.join(project_dir, 'data')
X_desc_path = os.path.join(data_dir, 'X_descriptors.npy')
X_fp_path = os.path.join(data_dir, 'X_fingerprint.npy')
y_path = os.path.join(data_dir, 'y_labels.npy')
smiles_path = os.path.join(data_dir, 'smiles_clean.npy')

# 随机种子，保证结果可复现
SEED = 42


def load_data():
    """加载特征和标签"""
    X_desc = np.load(X_desc_path)
    X_fp = np.load(X_fp_path)
    y = np.load(y_path)
    smiles = np.load(smiles_path)
    return X_desc, X_fp, y, smiles


def get_model(model_type, **kwargs):
    """获取分类模型"""
    if model_type == 'rf':
        return RandomForestClassifier(
            n_estimators=kwargs.get('n_estimators', 200),
            random_state=SEED,
            n_jobs=-1,
        )
    elif model_type == 'svm':
        return SVC(
            kernel=kwargs.get('kernel', 'rbf'),
            probability=True,
            random_state=SEED,
        )
    elif model_type == 'xgb':
        try:
            from xgboost import XGBClassifier
            return XGBClassifier(
                n_estimators=kwargs.get('n_estimators', 200),
                learning_rate=kwargs.get('learning_rate', 0.1),
                max_depth=kwargs.get('max_depth', 6),
                random_state=SEED,
                use_label_encoder=False,
                eval_metric='logloss',
            )
        except ImportError:
            raise ImportError('请先安装 xgboost: pip install xgboost')
    else:
        raise ValueError(f'不支持的模型类型: {model_type}')


def evaluate_classification(y_true, y_pred, y_prob=None):
    """评估分类模型，返回指标字典"""
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1': f1_score(y_true, y_pred, zero_division=0),
    }
    if y_prob is not None:
        metrics['roc_auc'] = roc_auc_score(y_true, y_prob)

    cm = confusion_matrix(y_true, y_pred)
    metrics['confusion_matrix'] = cm

    return metrics


def print_metrics(metrics, title=''):
    """打印评估指标"""
    if title:
        print(f'\n--- {title} ---')
    print(f"准确率 (Accuracy):  {metrics['accuracy']:.3f}")
    print(f"精确率 (Precision): {metrics['precision']:.3f}")
    print(f"召回率 (Recall):    {metrics['recall']:.3f}")
    print(f"F1 分数:           {metrics['f1']:.3f}")
    if 'roc_auc' in metrics:
        print(f"ROC-AUC:          {metrics['roc_auc']:.3f}")

    cm = metrics['confusion_matrix']
    print(f"\n混淆矩阵:")
    print(f"  真阴性(TN): {cm[0][0]:4d}  假阳性(FP): {cm[0][1]:4d}")
    print(f"  假阴性(FN): {cm[1][0]:4d}  真阳性(TP): {cm[1][1]:4d}")


def train_and_evaluate(X_train, X_test, y_train, y_test, model_type, feature_name, split_name):
    """训练模型并评估"""
    print(f'\n{"="*50}')
    print(f'模型: {model_type.upper()} | 特征: {feature_name} | 划分: {split_name}')
    print(f'{"="*50}')

    # 训练
    t0 = time.time()    # 记开始时间
    model = get_model(model_type)
    model.fit(X_train, y_train)
    train_time = time.time() - t0   # 算耗时
    print(f'训练耗时: {train_time:.2f}s')

    # 预测
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # 概率（用于 AUC）
    if hasattr(model, 'predict_proba'):
        y_prob_train = model.predict_proba(X_train)[:, 1]
        y_prob_test = model.predict_proba(X_test)[:, 1]
    else:
        y_prob_train = None
        y_prob_test = None

    # 评估
    metrics_train = evaluate_classification(y_train, y_pred_train, y_prob_train)
    metrics_test = evaluate_classification(y_test, y_pred_test, y_prob_test)

    print_metrics(metrics_train, title='训练集')
    print_metrics(metrics_test, title='测试集')

    # 过拟合程度
    overfit = metrics_train['accuracy'] - metrics_test['accuracy']
    print(f'\n过拟合程度(训练-测试准确率差): {overfit:.3f}')

    return model, metrics_train, metrics_test


def main():
    print('=' * 50)
    print('第4步：模型训练与评估')
    print('=' * 50)

    # 1. 加载数据
    print(f'\n加载数据...')
    X_desc, X_fp, y, smiles = load_data()
    print(f'总样本数: {len(y)}')
    print(f'活性: {y.sum()}  非活性: {len(y) - y.sum()}')

    # 2. 准备三种特征组合
    feature_sets = {
        '描述符(7维)': X_desc,
        '指纹(2048维)': X_fp,
        '描述符+指纹': np.hstack([X_desc, X_fp]),
    }

    # 3. 两种划分方式
    split_methods = {
        '随机划分': lambda: train_test_split(
            np.arange(len(y)), test_size=0.2, random_state=SEED, stratify=y
        ),
        '骨架划分': lambda: scaffold_split(smiles.tolist(), test_size=0.2, seed=SEED),
    }

    # 4. 三种模型
    model_types = ['rf', 'xgb', 'svm']

    # 5. 遍历所有组合，保存最佳结果
    all_results = []
    best_result = None  # (model, metrics, feature_name, split_name, model_type)

    for split_name, split_func in split_methods.items():
        train_idx, test_idx = split_func()

        for feat_name, X in feature_sets.items():
            X_train = X[train_idx]
            X_test = X[test_idx]
            y_train = y[train_idx]
            y_test = y[test_idx]

            for model_type in model_types:
                try:
                    model, m_train, m_test = train_and_evaluate(
                        X_train, X_test, y_train, y_test,
                        model_type, feat_name, split_name
                    )
                    all_results.append({
                        'model': model_type,
                        'feature': feat_name,
                        'split': split_name,
                        'test_acc': m_test['accuracy'],
                        'test_f1': m_test['f1'],
                        'test_auc': m_test.get('roc_auc', -1),
                        'overfit': m_train['accuracy'] - m_test['accuracy'],
                    })

                    # 记录最佳（按测试集 F1 排序）
                    if best_result is None or m_test['f1'] > best_result[1]['f1']:
                        best_result = (model, m_test, feat_name, split_name, model_type)

                except Exception as e:
                    print(f'\n  [跳过] {model_type} 出错: {e}')

    # 6. 汇总结果表
    print(f'\n\n{"="*70}')
    print('结果汇总（按测试集 F1 降序）')
    print(f'{"="*70}')

    # 按测试集 F1 排序
    all_results.sort(key=lambda x: x['test_f1'], reverse=True)

    header = f"{'模型':<6} {'特征':<14} {'划分':<8} {'准确率':>6} {'F1':>6} {'AUC':>6} {'过拟合':>6}"
    print(header)
    print('-' * 70)
    for r in all_results:
        auc_str = f"{r['test_auc']:.3f}" if r['test_auc'] > 0 else "N/A"
        print(f"{r['model']:<6} {r['feature']:<14} {r['split']:<8} "
              f"{r['test_acc']:>6.3f} {r['test_f1']:>6.3f} {auc_str:>6} {r['overfit']:>6.3f}")

    # 7. 最佳模型
    if best_result:
        best_model, best_metrics, best_feat, best_split, best_mtype = best_result
        print(f'\n🏆 最佳模型: {best_mtype.upper()} + {best_feat} + {best_split}')
        print(f'   测试集 F1 = {best_metrics["f1"]:.3f}, AUC = {best_metrics.get("roc_auc", -1):.3f}')


if __name__ == '__main__':
    main()
