import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy import stats
import json, os

egfr_path = r'C:\Users\JJFY\Desktop\AIDD-learing\projects\egfr\data\descriptors.csv'
cox2_path = r'C:\Users\JJFY\Desktop\AIDD-learing\projects\cox2\data\descriptors.csv'
fig_dir = r'C:\Users\JJFY\Desktop\AIDD-learing\projects\cox2\figures\comparison'
os.makedirs(fig_dir, exist_ok=True)

df_egfr = pd.read_csv(egfr_path)
df_cox2 = pd.read_csv(cox2_path)
df_egfr['target'] = 'EGFR'
df_cox2['target'] = 'COX-2'
df_all = pd.concat([df_egfr, df_cox2], ignore_index=True)

descs = ['MolWt', 'MolLogP', 'NumHAcceptors', 'NumHDonors', 'TPSA', 'NumRotatableBonds', 'FractionCSP3']
labels_cn = {
    'MolWt': 'Molecular Weight',
    'MolLogP': 'LogP',
    'NumHAcceptors': 'HBA',
    'NumHDonors': 'HBD',
    'TPSA': 'TPSA',
    'NumRotatableBonds': 'Rotatable Bonds',
    'FractionCSP3': 'Fsp3',
}

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.facecolor': '#1a1a1a',
    'figure.facecolor': '#1a1a1a',
    'axes.edgecolor': '#888888',
    'axes.labelcolor': '#cccccc',
    'xtick.color': '#aaaaaa',
    'ytick.color': '#aaaaaa',
    'axes.grid': True,
    'grid.color': '#333333',
    'grid.alpha': 0.3,
})

results = []
for d in descs:
    e_vals = df_egfr[d].dropna()
    c_vals = df_cox2[d].dropna()

    stat_u, p_val = stats.mannwhitneyu(e_vals, c_vals, alternative='two-sided')

    pooled = np.concatenate([e_vals, c_vals])
    n1, n2 = len(e_vals), len(c_vals)
    rank_biserial = 1 - (2 * stat_u) / (n1 * n2)

    e_active = df_egfr[df_egfr['label'] == 1][d].dropna()
    e_inactive = df_egfr[df_egfr['label'] == 0][d].dropna()
    c_active = df_cox2[df_cox2['label'] == 1][d].dropna()
    c_inactive = df_cox2[df_cox2['label'] == 0][d].dropna()

    results.append({
        'descriptor': d,
        'label': labels_cn[d],
        'egfr_mean': round(e_vals.mean(), 2),
        'egfr_median': round(e_vals.median(), 2),
        'egfr_std': round(e_vals.std(), 2),
        'cox2_mean': round(c_vals.mean(), 2),
        'cox2_median': round(c_vals.median(), 2),
        'cox2_std': round(c_vals.std(), 2),
        'diff_mean': round(e_vals.mean() - c_vals.mean(), 2),
        'p_value': round(p_val, 6),
        'effect_size': round(abs(rank_biserial), 3),
        'significant': bool(p_val < 0.05),
        'egfr_active_mean': round(e_active.mean(), 2),
        'egfr_inactive_mean': round(e_inactive.mean(), 2),
        'cox2_active_mean': round(c_active.mean(), 2),
        'cox2_inactive_mean': round(c_inactive.mean(), 2),
        'egfr_active_trend': 'up' if e_active.mean() > e_inactive.mean() else 'down' if e_active.mean() < e_inactive.mean() else 'flat',
        'cox2_active_trend': 'up' if c_active.mean() > c_inactive.mean() else 'down' if c_active.mean() < c_inactive.mean() else 'flat',
    })

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()
for i, d in enumerate(descs):
    ax = axes[i]
    data = [df_egfr[d].dropna(), df_cox2[d].dropna()]
    bp = ax.boxplot(data, labels=['EGFR', 'COX-2'], patch_artist=True, widths=0.5)
    for patch in bp['boxes']:
        patch.set_facecolor('#444444')
        patch.set_alpha(0.7)
    for element in bp['medians']:
        element.set_color('#e0d5c1')
    ax.set_title(labels_cn[d], color='#e0d5c1', fontsize=12, fontweight='bold')
    ax.set_ylabel(labels_cn[d], color='#aaaaaa')
axes[7].set_visible(False)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'boxplot_all.png'), dpi=150, facecolor='#1a1a1a')
plt.close()

fig, axes = plt.subplots(2, 4, figsize=(18, 9))
axes = axes.flatten()
for i, d in enumerate(descs):
    ax = axes[i]
    data = [
        df_egfr[df_egfr['label'] == 1][d].dropna(),
        df_egfr[df_egfr['label'] == 0][d].dropna(),
        df_cox2[df_cox2['label'] == 1][d].dropna(),
        df_cox2[df_cox2['label'] == 0][d].dropna(),
    ]
    bp = ax.boxplot(data, labels=['EGFR+', 'EGFR-', 'COX2+', 'COX2-'], patch_artist=True, widths=0.5)
    colors = ['#8b7355', '#555555', '#8b7355', '#555555']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    for element in bp['medians']:
        element.set_color('#e0d5c1')
    ax.set_title(labels_cn[d], color='#e0d5c1', fontsize=11, fontweight='bold')
axes[7].set_visible(False)
plt.tight_layout()
fig.savefig(os.path.join(fig_dir, 'boxplot_by_activity.png'), dpi=150, facecolor='#1a1a1a')
plt.close()

stats_path = os.path.join(fig_dir, 'stats.json')
with open(stats_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('Done! Charts and stats saved to:', fig_dir)
