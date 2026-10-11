"""
第5步：结果可视化与深度分析
- ROC 曲线对比
- 混淆矩阵热力图
- 特征重要性（RF / XGB）
- 错误样本分析（哪些分子被预测错了？）
- 描述符分布对比（活性 vs 非活性）
用法：python 05_visualize_analyze.py
"""

import numpy as np
import os
import sys
import matplotlib
matplotlib.use('Agg')  # 不显示图形界面，直接保存图片
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 把项目根目录加到路径里
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(script_dir, '..')
sys.path.insert(0, project_dir)

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, confusion_matrix

# 尝试导入中文字体
def setup_chinese_font():
    """尝试设置中文字体"""
    font_candidates = [
        'Microsoft YaHei',     # Windows
        'SimHei',              # Windows 黑体
        'PingFang SC',         # macOS
        'Noto Sans CJK SC',    # Linux
        'WenQuanYi Micro Hei', # Linux
        'Arial Unicode MS',    # 通用备选
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for font in font_candidates:
        if font in available:
            plt.rcParams['font.sans-serif'] = [font]
            plt.rcParams['axes.unicode_minus'] = False
            return font
    return None

chinese_font = setup_chinese_font()

# 文件路径
data_dir = os.path.join(project_dir, 'data')
fig_dir = os.path.join(project_dir, 'figures')
os.makedirs(fig_dir, exist_ok=True)

X_desc_path = os.path.join(data_dir, 'X_descriptors.npy')
X_fp_path = os.path.join(data_dir, 'X_fingerprint.npy')
y_path = os.path.join(data_dir, 'y_labels.npy')
smiles_path = os.path.join(data_dir, 'smiles_clean.npy')

SEED = 42

# 描述符名称
DESC_NAMES = ['MolWt', 'MolLogP', 'NumHAcceptors', 'NumHDonors',
              'TPSA', 'NumRotatableBonds', 'FractionCSP3']

# 描述符中文名
DESC_NAMES_CN = {
    'MolWt': '分子量',
    'MolLogP': '脂水分配系数 (LogP)',
    'NumHAcceptors': '氢键受体数',
    'NumHDonors': '氢键给体数',
    'TPSA': '拓扑极性表面积',
    'NumRotatableBonds': '可旋转键数',
    'FractionCSP3': 'sp3碳比例 (Fsp3)',
}


def load_data():
    """加载特征和标签"""
    X_desc = np.load(X_desc_path)
    X_fp = np.load(X_fp_path)
    y = np.load(y_path)
    smiles = np.load(smiles_path)
    return X_desc, X_fp, y, smiles


def plot_roc_curves(models_data, title='ROC 曲线对比', filename='roc_curves.png'):
    """画多个模型的 ROC 曲线对比"""
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = ['#B8551D', '#F59E42', '#8E6E63', '#D97757']
    for i, (name, y_true, y_prob) in enumerate(models_data):
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=colors[i % len(colors)], lw=2,
                label=f'{name} (AUC = {roc_auc:.3f})')

    ax.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5, label='随机猜测 (AUC = 0.5)')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('假阳性率 (False Positive Rate)', fontsize=12)
    ax.set_ylabel('真阳性率 (True Positive Rate)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  已保存: {filename}')


def plot_confusion_matrix_heatmap(cm, title='混淆矩阵', filename='confusion_matrix.png',
                                   labels=['非活性', '活性']):
    """画混淆矩阵热力图"""
    fig, ax = plt.subplots(figsize=(6, 5))

    # 归一化（按行）
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    im = ax.imshow(cm_norm, interpolation='nearest', cmap=plt.cm.Oranges, vmin=0, vmax=1)
    ax.figure.colorbar(im, ax=ax, label='比例')

    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=labels,
           yticklabels=labels)
    ax.set_xlabel('预测标签', fontsize=12)
    ax.set_ylabel('真实标签', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    # 在每个格子里写数字（绝对值 + 百分比）
    thresh = cm_norm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            text_color = 'white' if cm_norm[i, j] > thresh else 'black'
            ax.text(j, i, f'{cm[i, j]}\n({cm_norm[i, j]:.1%})',
                    ha='center', va='center', color=text_color, fontsize=11)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  已保存: {filename}')


def plot_feature_importance(importances, feature_names, title='特征重要性',
                            filename='feature_importance.png', top_n=20):
    """画特征重要性柱状图（Top N）"""
    # 排序
    indices = np.argsort(importances)[::-1]
    top_indices = indices[:top_n]
    top_names = [feature_names[i] for i in top_indices]
    top_importances = importances[top_indices]

    fig, ax = plt.subplots(figsize=(10, max(4, top_n * 0.35)))

    y_pos = np.arange(len(top_names))
    bars = ax.barh(y_pos, top_importances, color='#B8551D', alpha=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_names, fontsize=9)
    ax.set_xlabel('重要性得分', fontsize=11)
    ax.set_title(f'{title} (Top {top_n})', fontsize=13, fontweight='bold')
    ax.invert_yaxis()  # 最重要的在上面
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  已保存: {filename}')


def plot_descriptor_distribution(X_desc, y, desc_idx, desc_name, filename=None):
    """画单个描述符在活性/非活性组的分布对比"""
    active = X_desc[y == 1, desc_idx]
    inactive = X_desc[y == 0, desc_idx]

    fig, ax = plt.subplots(figsize=(8, 5))

    # 画直方图
    bins = 30
    ax.hist(inactive, bins=bins, alpha=0.6, label=f'非活性 (n={len(inactive)})',
            color='#8E6E63', density=True, edgecolor='white')
    ax.hist(active, bins=bins, alpha=0.6, label=f'活性 (n={len(active)})',
            color='#B8551D', density=True, edgecolor='white')

    # 画均值线
    ax.axvline(np.mean(inactive), color='#8E6E63', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.axvline(np.mean(active), color='#B8551D', linestyle='--', linewidth=1.5, alpha=0.8)

    cn_name = DESC_NAMES_CN.get(desc_name, desc_name)
    ax.set_xlabel(cn_name, fontsize=11)
    ax.set_ylabel('密度', fontsize=11)
    ax.set_title(f'{cn_name} 分布对比', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # 添加均值标注
    ax.text(0.02, 0.95, f'非活性均值: {np.mean(inactive):.2f}\n活性均值: {np.mean(active):.2f}',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    if filename is None:
        filename = f'dist_{desc_name}.png'

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, filename), dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  已保存: {filename}')


def analyze_errors(X_desc, y_true, y_pred, smiles, desc_names):
    """分析错误样本：假阳性和假阴性的描述符统计"""
    fp_mask = (y_true == 0) & (y_pred == 1)  # 假阳性：预测成活性，实际非活性
    fn_mask = (y_true == 1) & (y_pred == 0)  # 假阴性：预测成非活性，实际活性

    print(f'\n--- 错误样本分析 ---')
    print(f'假阳性 (FP): {fp_mask.sum()} 个（实际非活性，被预测为活性）')
    print(f'假阴性 (FN): {fn_mask.sum()} 个（实际活性，被预测为非活性）')

    # 描述符统计对比
    print(f'\n描述符均值对比：')
    print(f"{'描述符':<20} {'FP组':>10} {'FN组':>10} {'全体':>10}")
    print('-' * 55)
    for i, name in enumerate(desc_names):
        fp_mean = np.mean(X_desc[fp_mask, i]) if fp_mask.sum() > 0 else 0
        fn_mean = np.mean(X_desc[fn_mask, i]) if fn_mask.sum() > 0 else 0
        all_mean = np.mean(X_desc[:, i])
        cn_name = DESC_NAMES_CN.get(name, name)
        print(f'{cn_name:<20} {fp_mean:>10.2f} {fn_mean:>10.2f} {all_mean:>10.2f}')

    # 打印一些 FP 和 FN 的 SMILES 示例
    if fp_mask.sum() > 0:
        print(f'\n假阳性示例（前 5 个）：')
        fp_smiles_list = smiles[fp_mask][:5]
        for i, smi in enumerate(fp_smiles_list):
            print(f'  {i+1}. {smi}')

    if fn_mask.sum() > 0:
        print(f'\n假阴性示例（前 5 个）：')
        fn_smiles_list = smiles[fn_mask][:5]
        for i, smi in enumerate(fn_smiles_list):
            print(f'  {i+1}. {smi}')


def main():
    print('=' * 50)
    print('第5步：结果可视化与深度分析')
    print('=' * 50)

    if chinese_font:
        print(f'\n使用中文字体: {chinese_font}')
    else:
        print('\n⚠️  未找到中文字体，图表中可能显示方块')

    # 1. 加载数据
    print(f'\n加载数据...')
    X_desc, X_fp, y, smiles = load_data()
    print(f'总样本数: {len(y)}，活性: {y.sum()}，非活性: {len(y)-y.sum()}')

    # 2. 划分数据集（随机划分，用于画图）
    X_train_fp, X_test_fp, y_train, y_test, idx_train, idx_test = train_test_split(
        X_fp, y, np.arange(len(y)), test_size=0.2, random_state=SEED, stratify=y
    )
    X_train_desc = X_desc[idx_train]
    X_test_desc = X_desc[idx_test]
    smiles_test = smiles[idx_test]

    # 3. 训练几个代表性模型，用于画图
    print(f'\n训练模型（用于可视化）...')

    # 3.1 RF + 指纹
    rf_fp = RandomForestClassifier(n_estimators=200, random_state=SEED, n_jobs=-1)
    rf_fp.fit(X_train_fp, y_train)
    y_pred_rf_fp = rf_fp.predict(X_test_fp)
    y_prob_rf_fp = rf_fp.predict_proba(X_test_fp)[:, 1]

    # 3.2 RF + 描述符
    rf_desc = RandomForestClassifier(n_estimators=200, random_state=SEED, n_jobs=-1)
    rf_desc.fit(X_train_desc, y_train)
    y_pred_rf_desc = rf_desc.predict(X_test_desc)
    y_prob_rf_desc = rf_desc.predict_proba(X_test_desc)[:, 1]

    # 3.3 SVM + 指纹
    svm_fp = SVC(kernel='rbf', probability=True, random_state=SEED)
    svm_fp.fit(X_train_fp, y_train)
    y_pred_svm_fp = svm_fp.predict(X_test_fp)
    y_prob_svm_fp = svm_fp.predict_proba(X_test_fp)[:, 1]

    # 4. 画图
    print(f'\n生成图表，保存到: {fig_dir}')

    # 4.1 ROC 曲线对比
    print(f'\n[1/5] ROC 曲线')
    plot_roc_curves([
        ('RF + 指纹', y_test, y_prob_rf_fp),
        ('RF + 描述符', y_test, y_prob_rf_desc),
        ('SVM + 指纹', y_test, y_prob_svm_fp),
    ], title='不同模型 ROC 曲线对比（随机划分）', filename='roc_comparison.png')

    # 4.2 混淆矩阵
    print(f'\n[2/5] 混淆矩阵')
    cm_rf_fp = confusion_matrix(y_test, y_pred_rf_fp)
    plot_confusion_matrix_heatmap(cm_rf_fp, title='RF + 指纹 混淆矩阵',
                                   filename='cm_rf_fingerprint.png')

    cm_rf_desc = confusion_matrix(y_test, y_pred_rf_desc)
    plot_confusion_matrix_heatmap(cm_rf_desc, title='RF + 描述符 混淆矩阵',
                                   filename='cm_rf_descriptors.png')

    # 4.3 描述符特征重要性
    print(f'\n[3/5] 描述符特征重要性')
    plot_feature_importance(
        rf_desc.feature_importances_,
        [DESC_NAMES_CN.get(n, n) for n in DESC_NAMES],
        title='描述符特征重要性 (RF)',
        filename='feature_importance_desc.png',
        top_n=7
    )

    # 4.4 指纹特征重要性（Top 20）
    print(f'\n[4/5] 指纹特征重要性 (Top 20)')
    fp_feature_names = [f'Bit_{i}' for i in range(2048)]
    plot_feature_importance(
        rf_fp.feature_importances_,
        fp_feature_names,
        title='Morgan 指纹特征重要性 (RF)',
        filename='feature_importance_fp.png',
        top_n=20
    )

    # 4.5 描述符分布对比
    print(f'\n[5/5] 描述符分布对比（活性 vs 非活性）')
    for i, name in enumerate(DESC_NAMES):
        plot_descriptor_distribution(X_desc, y, i, name)

    # 5. 错误样本分析
    print(f'\n错误样本分析（RF + 指纹）')
    analyze_errors(X_test_desc, y_test, y_pred_rf_fp, smiles_test, DESC_NAMES)

    # 6. 总结
    print(f'\n{"="*50}')
    print('分析完成！所有图表保存在:')
    print(f'  {fig_dir}')
    print(f'\n生成的文件:')
    for f in sorted(os.listdir(fig_dir)):
        print(f'  - {f}')


if __name__ == '__main__':
    main()
