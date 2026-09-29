"""
第3步：训练模型 + 评估 + 三种特征策略对比
用法：python 03_train_eval.py

模型：随机森林、XGBoost
评估：AUROC、AUPRC、F1、Accuracy
输出：结果对比表 + ROC曲线图
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    f1_score, accuracy_score, roc_curve
)

script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, '..', 'results')


def load_features(split_name, strategy):
    path = os.path.join(results_dir, f'{split_name}_{strategy}.npz')
    if not os.path.exists(path):
        print(f'特征文件不存在: {path}')
        print('请先运行 02_pair_features.py')
        sys.exit(1)
    data = np.load(path)
    return data['X'], data['y']


def train_rf(X_train, y_train, n_estimators=200, random_state=42):
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def train_xgb(X_train, y_train, random_state=42):
    try:
        from xgboost import XGBClassifier
        model = XGBClassifier(
            random_state=random_state,
            eval_metric='logloss',
            use_label_encoder=False
        )
        model.fit(X_train, y_train)
        return model
    except ImportError:
        print('  XGBoost未安装，跳过')
        return None


def evaluate(model, X_test, y_test):
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    auroc = roc_auc_score(y_test, y_proba)
    auprc = average_precision_score(y_test, y_proba)
    f1 = f1_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)

    return {
        'AUROC': auroc,
        'AUPRC': auprc,
        'F1': f1,
        'ACC': acc
    }


def main():
    print('=' * 50)
    print('第3步：训练 + 评估 + 策略对比')
    print('=' * 50)

    strategies = ['concat', 'tensor_prod', 'difference']
    models = ['RF', 'XGB']
    all_results = []

    for strategy in strategies:
        print(f'\n--- 特征策略: {strategy} ---')

        X_train, y_train = load_features('train', strategy)
        X_val, y_val = load_features('val', strategy)
        X_test, y_test = load_features('test', strategy)

        print(f'  train={X_train.shape}, val={X_val.shape}, test={X_test.shape}')

        for model_name in models:
            print(f'\n  模型: {model_name}')

            if model_name == 'RF':
                model = train_rf(X_train, y_train)
            else:
                model = train_xgb(X_train, y_train)
                if model is None:
                    continue

            metrics = evaluate(model, X_test, y_test)
            metrics['strategy'] = strategy
            metrics['model'] = model_name
            all_results.append(metrics)

            print(f'    AUROC={metrics["AUROC"]:.4f}  AUPRC={metrics["AUPRC"]:.4f}  '
                  f'F1={metrics["F1"]:.4f}  ACC={metrics["ACC"]:.4f}')

            fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
            plt.plot(fpr, tpr, label=f'{strategy}-{model_name} (AUC={metrics["AUROC"]:.3f})')

    plt.plot([0, 1], [0, 1], 'k--', alpha=0.3)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('DDI Prediction - ROC Curves')
    plt.legend(loc='lower right', fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'roc_comparison.png'), dpi=150)
    plt.close()

    df_results = pd.DataFrame(all_results)
    df_results = df_results[['strategy', 'model', 'AUROC', 'AUPRC', 'F1', 'ACC']]
    df_results.to_csv(os.path.join(results_dir, 'comparison_results.csv'), index=False)

    print('\n' + '=' * 50)
    print('结果对比汇总')
    print('=' * 50)
    print(df_results.to_string(index=False))
    print(f'\nROC曲线已保存到 {results_dir}/roc_comparison.png')
    print(f'结果表格已保存到 {results_dir}/comparison_results.csv')


if __name__ == '__main__':
    main()
