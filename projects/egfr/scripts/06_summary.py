"""
第6步：项目总结报告
生成 EGFR QSAR 项目的完整总结，包含：
- 项目流程回顾
- 数据概况
- 模型结果汇总
- 药学发现
- 英文术语表
- 下一步建议
用法：python 06_summary.py
"""

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(script_dir, '..')
report_path = os.path.join(project_dir, 'EGFR_QSAR_summary.html')


def main():
    print('=' * 50)
    print('第6步：项目总结报告')
    print('=' * 50)

    html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EGFR QSAR 项目总结</title>
<style>
:root {
  --bg: #101011;
  --card-bg: #18181a;
  --card-border: #2a2a2d;
  --text: #e0ddd8;
  --text-dim: #8a8680;
  --accent: #b8551d;
  --accent-dim: #8e6e63;
  --code-bg: #1e1e20;
  --border: #333335;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Instrument Sans', 'Segoe UI', system-ui, sans-serif;
  line-height: 1.7;
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}
h1, h2, h3 {
  font-family: 'Bricolage Grotesque', 'Segoe UI', system-ui, sans-serif;
  font-weight: 700;
}
h1 {
  font-size: 2rem;
  margin-bottom: 8px;
  color: var(--text);
}
h2 {
  font-size: 1.4rem;
  margin-top: 48px;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
  color: var(--accent);
}
h3 {
  font-size: 1.1rem;
  margin-top: 28px;
  margin-bottom: 12px;
  color: var(--text-dim);
}
.subtitle {
  color: var(--text-dim);
  font-size: 0.9rem;
  font-family: 'Geist Mono', 'Courier New', monospace;
  margin-bottom: 40px;
}
.card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
}
.card-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent);
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 0.92rem;
}
th, td {
  text-align: left;
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
}
th {
  color: var(--accent-dim);
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
td {
  color: var(--text);
}
tr:hover {
  background: var(--code-bg);
}
code {
  font-family: 'Geist Mono', 'Courier New', monospace;
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.88rem;
  color: var(--accent);
}
.highlight {
  color: var(--accent);
  font-weight: 600;
}
.tag {
  display: inline-block;
  font-family: 'Geist Mono', monospace;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 3px;
  background: var(--code-bg);
  color: var(--text-dim);
  border: 1px solid var(--border);
  margin: 2px;
}
.tags {
  margin: 8px 0;
}
.note {
  border-left: 3px solid var(--accent);
  padding: 12px 16px;
  margin: 16px 0;
  background: var(--code-bg);
  border-radius: 0 4px 4px 0;
  font-size: 0.92rem;
}
.note-title {
  color: var(--accent);
  font-weight: 600;
  margin-bottom: 4px;
}
ul, ol {
  margin-left: 20px;
  margin-bottom: 12px;
}
li {
  margin-bottom: 6px;
}
.footer {
  margin-top: 48px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
  color: var(--text-dim);
  font-size: 0.85rem;
  font-family: 'Geist Mono', monospace;
  text-align: center;
}
</style>
</head>
<body>

<h1>EGFR QSAR 项目总结</h1>
<p class="subtitle">Epidermal Growth Factor Receptor · Quantitative Structure-Activity Relationship · 2026.09–2026.10</p>

<div class="tags">
  <span class="tag">ChEMBL</span>
  <span class="tag">RDKit</span>
  <span class="tag">Morgan Fingerprint</span>
  <span class="tag">Random Forest</span>
  <span class="tag">SVM</span>
  <span class="tag">XGBoost</span>
  <span class="tag">Scaffold Split</span>
  <span class="tag">Binary Classification</span>
</div>

<!-- ==================== 项目流程 ==================== -->

<h2>项目流程</h2>

<div class="card">
<div class="card-title">Pipeline Overview</div>
<table>
<tr><th>步骤</th><th>脚本</th><th>内容</th><th>输出</th></tr>
<tr><td>1</td><td><code>01_fetch_data.py</code></td><td>从 ChEMBL 拉取 EGFR 活性数据</td><td>egfr_raw.csv (5000条)</td></tr>
<tr><td>2</td><td><code>02_clean_data.py</code></td><td>数据清洗：去空值、标准化 SMILES、去重、定义标签</td><td>egfr_clean.csv (2032个唯一分子)</td></tr>
<tr><td>3</td><td><code>03_calculate_features.py</code></td><td>计算分子描述符(7维) + Morgan指纹(2048维)</td><td>.npy 文件 (2030个分子)</td></tr>
<tr><td>4</td><td><code>04_train_evaluate.py</code></td><td>3特征 × 2划分 × 3模型 = 18种组合训练评估</td><td>结果汇总表</td></tr>
<tr><td>5</td><td><code>05_visualize_analyze.py</code></td><td>ROC曲线、混淆矩阵、特征重要性、描述符分布</td><td>12张图 + 错误分析</td></tr>
<tr><td>6</td><td><code>06_summary.py</code></td><td>项目总结报告（本文件）</td><td>HTML 报告</td></tr>
</table>
</div>

<!-- ==================== 数据概况 ==================== -->

<h2>数据概况</h2>

<div class="card">
<div class="card-title">Data Summary</div>
<table>
<tr><th>指标</th><th>数值</th><th>说明</th></tr>
<tr><td>原始数据</td><td>5,000 条</td><td>从 ChEMBL 拉取的 EGFR 活性记录</td></tr>
<tr><td>去空 pChEMBL 后</td><td>3,131 条</td><td>近 2000 条无精确活性值</td></tr>
<tr><td>去重后</td><td>2,032 个唯一分子</td><td>SMILES 标准化后去重</td></tr>
<tr><td>过滤异常值后</td><td>2,030 个</td><td>去掉 MW > 1000 的 2 个分子</td></tr>
<tr><td>活性分子 (label=1)</td><td>1,053 (51.9%)</td><td>pChEMBL >= 6.5 (IC50 <= ~316 nM)</td></tr>
<tr><td>非活性分子 (label=0)</td><td>977 (48.1%)</td><td>pChEMBL < 6.5</td></tr>
<tr><td>正负比例</td><td>~1:1</td><td>均衡，无需过采样/欠采样</td></tr>
</table>

<div class="note">
<div class="note-title">为什么选 pChEMBL 6.5 做阈值？</div>
pChEMBL = -log10(IC50 in M)。6.5 对应 IC50 ≈ 316 nM ≈ 0.3 μM。药物化学中一般以 IC50 < 1 μM (pChEMBL > 6) 作为"有活性"的门槛，6.5 是更严格的标准。EGFR 临床抑制剂（如吉非替尼、厄洛替尼）的 IC50 都在 nM 级别，6.5 的阈值能合理区分先导化合物和真正有潜力的候选。
</div>
</div>

<!-- ==================== 模型结果 ==================== -->

<h2>模型结果汇总</h2>

<div class="card">
<div class="card-title">Top 5 Models (by Test F1, Scaffold Split)</div>
<table>
<tr><th>#</th><th>模型</th><th>特征</th><th>划分</th><th>Accuracy</th><th>F1</th><th>AUC</th><th>过拟合</th></tr>
<tr><td>1</td><td>SVM</td><td>指纹(2048维)</td><td>骨架划分</td><td>0.850</td><td class="highlight">0.912</td><td>0.838</td><td>0.047</td></tr>
<tr><td>2</td><td>XGB</td><td>描述符+指纹</td><td>骨架划分</td><td>0.847</td><td>0.910</td><td>0.828</td><td>0.132</td></tr>
<tr><td>3</td><td>RF</td><td>指纹(2048维)</td><td>骨架划分</td><td>0.837</td><td>0.905</td><td>0.811</td><td>0.159</td></tr>
<tr><td>4</td><td>XGB</td><td>指纹(2048维)</td><td>骨架划分</td><td>0.833</td><td>0.904</td><td>0.798</td><td>0.121</td></tr>
<tr><td>5</td><td>RF</td><td>描述符+指纹</td><td>骨架划分</td><td>0.833</td><td>0.903</td><td>0.820</td><td>0.160</td></tr>
</table>
</div>

<div class="card">
<div class="card-title">Key Findings</div>

<h3>1. 指纹 >> 描述符</h3>
<p>只用 7 个理化描述符的模型 F1 约 0.5-0.7，加上 2048 维 Morgan 指纹后直接跳到 0.85-0.91。<span class="highlight">结构信息远比简单理化性质重要</span>——EGFR 活性主要由子结构模式决定，而非分子量和脂溶性。</p>

<h3>2. SVM 在指纹数据上表现最佳</h3>
<p>SVM + 指纹 + 骨架划分取得最高 F1 (0.912) 且过拟合最低 (0.047)。原因：Morgan 指纹是高维稀疏数据（2048维），SVM 在高维空间做间隔最大化（margin maximization）天生擅长这类数据。</p>

<h3>3. 随机划分 vs 骨架划分差距明显</h3>
<p>以 XGB + 指纹为例：随机划分 AUC=0.927，骨架划分 AUC=0.798，掉了 0.13。随机划分因训练集和测试集有相似骨架，模型容易"作弊"。骨架划分更接近真实药物发现场景——新化合物的骨架通常与训练数据不同。</p>

<h3>4. 描述符模型的骨架划分结果接近随机</h3>
<p>RF + 描述符 + 骨架划分：准确率 0.571，过拟合 0.407。7 个粗粒度参数完全无法捕捉骨架差异，模型只是"记住"了见过的骨架模式。</p>
</div>

<!-- ==================== 药学发现 ==================== -->

<h2>药学发现</h2>

<div class="card">
<div class="card-title">EGFR Inhibitor Molecular Profile</div>
<table>
<tr><th>描述符</th><th>非活性均值</th><th>活性均值</th><th>方向</th><th>药学意义</th></tr>
<tr><td>MolWt (分子量)</td><td>396</td><td>425</td><td>↑</td><td>需要足够大才能占据 ATP 结合口袋</td></tr>
<tr><td>MolLogP (脂水性)</td><td>3.95</td><td>4.25</td><td>↑</td><td>口袋内有疏水残基（Leu, Val, Ala），需疏水分子</td></tr>
<tr><td>TPSA (极性表面积)</td><td>89</td><td>81</td><td>↓</td><td>极性要低以保证透膜性（EGFR 在细胞内侧）</td></tr>
<tr><td>NumHDonors (氢键给体)</td><td>2.22</td><td>1.94</td><td>↓</td><td>给体少 → 透膜好 + 结合主要靠受体而非给体</td></tr>
<tr><td>NumHAcceptors (氢键受体)</td><td>5.47</td><td>5.96</td><td>↑</td><td>略多，与 hinge 区形成关键氢键需要</td></tr>
<tr><td>NumRotatableBonds (可旋转键)</td><td>5.34</td><td>6.06</td><td>↑</td><td>需要灵活性适应细长的 ATP 口袋形状</td></tr>
<tr><td>FractionCSP3 (sp3碳比例)</td><td>0.17</td><td>0.18</td><td>—</td><td>无区分度（同一靶点骨架都偏平面）</td></tr>
</table>

<div class="note">
<div class="note-title">一句话总结</div>
EGFR 活性抑制剂的分子画像：<span class="highlight">大一些、疏水一些、极性低一些、氢键给体少一些</span>。这与激酶抑制剂的药理学认知完全一致——需要足够大的疏水分子进入细胞内结合 ATP 口袋，但极性不能太高以保证口服透膜性。
</div>
</div>

<div class="card">
<div class="card-title">Error Analysis: 假阳性 vs 假阴性</div>
<table>
<tr><th>描述符</th><th>假阳性 (FP)</th><th>假阴性 (FN)</th><th>全体</th><th>说明</th></tr>
<tr><td>MolWt</td><td>440.5</td><td>351.3</td><td>410.9</td><td>FP 更大 → 模型偏好"大分子=活性"</td></tr>
<tr><td>MolLogP</td><td>4.50</td><td>3.78</td><td>4.12</td><td>FP 更疏水</td></tr>
<tr><td>NumHAcceptors</td><td>6.21</td><td>5.11</td><td>5.70</td><td>FP 受体更多</td></tr>
<tr><td>NumHDonors</td><td>1.62</td><td>2.05</td><td>2.07</td><td>FP 给体更少</td></tr>
<tr><td>NumRotatableBonds</td><td>6.62</td><td>4.74</td><td>5.72</td><td>FP 更灵活</td></tr>
</table>
<p>模型学到了"EGFR 抑制剂通常长什么样"的刻板印象，对跳出这个模式的活性分子（小而亲水）识别能力不足。这在虚拟筛选中意味着：模型可能漏掉具有 novel binding mode 的活性分子。</p>
</div>

<!-- ==================== 描述符重要性 ==================== -->

<h2>描述符特征重要性</h2>

<div class="card">
<div class="card-title">RF Feature Importance (Descriptors)</div>
<table>
<tr><th>排名</th><th>描述符</th><th>重要性</th><th>药学解释</th></tr>
<tr><td>1</td><td>MolLogP</td><td>~0.22</td><td>脂溶性是区分活性的关键 — 疏水口袋需要疏水分子</td></tr>
<tr><td>2</td><td>MolWt</td><td>~0.21</td><td>分子大小决定能否占据口袋</td></tr>
<tr><td>3</td><td>TPSA</td><td>~0.18</td><td>极性表面积影响透膜性</td></tr>
<tr><td>4</td><td>FractionCSP3</td><td>~0.14</td><td>排名虽高但实际区分度低（只有7个特征放大了相对值）</td></tr>
<tr><td>5</td><td>NumHAcceptors</td><td>~0.10</td><td>与 hinge 区结合相关</td></tr>
<tr><td>6</td><td>NumRotatableBonds</td><td>~0.09</td><td>灵活性影响口袋适配</td></tr>
<tr><td>7</td><td>NumHDonors</td><td>~0.08</td><td>最不重要 — 大家都有类似给体（喹唑啉骨架），区分度低</td></tr>
</table>
</div>

<!-- ==================== 英文术语表 ==================== -->

<h2>英文术语表</h2>

<div class="card">
<div class="card-title">Vocabulary</div>

<h3>Data & Descriptors</h3>
<table>
<tr><th>英文</th><th>中文</th><th>说明</th></tr>
<tr><td>SMILES</td><td>简化分子线性输入规范</td><td>用文本表示分子结构的标准</td></tr>
<tr><td>Canonical SMILES</td><td>规范SMILES</td><td>同一分子的唯一标准写法</td></tr>
<tr><td>Tautomer</td><td>互变异构体</td><td>质子位置不同但为同一分子的不同形态</td></tr>
<tr><td>pChEMBL</td><td>pChEMBL值</td><td>-log10(IC50 in M)，活性强度的对数表示</td></tr>
<tr><td>Standard Relation</td><td>标准关系</td><td>= 精确值, > 大于检测限, < 小于检测上限</td></tr>
<tr><td>Morgan Fingerprint</td><td>Morgan指纹</td><td>分子子结构的哈希位向量（ECFP4）</td></tr>
<tr><td>MolWt</td><td>分子量</td><td>Molecular Weight</td></tr>
<tr><td>MolLogP</td><td>脂水分配系数</td><td>LogP，疏水性的度量</td></tr>
<tr><td>TPSA</td><td>拓扑极性表面积</td><td>Topological Polar Surface Area</td></tr>
<tr><td>NumHDonors</td><td>氢键给体数</td><td>能提供氢键的 NH/OH 数量</td></tr>
<tr><td>NumHAcceptors</td><td>氢键受体数</td><td>能接受氢键的 N/O 数量</td></tr>
<tr><td>NumRotatableBonds</td><td>可旋转键数</td><td>分子灵活性的度量</td></tr>
<tr><td>FractionCSP3</td><td>sp3碳比例</td><td>Fsp3，分子立体程度的度量</td></tr>
</table>

<h3>Machine Learning</h3>
<table>
<tr><th>英文</th><th>中文</th><th>说明</th></tr>
<tr><td>QSAR</td><td>定量构效关系</td><td>Quantitative Structure-Activity Relationship</td></tr>
<tr><td>Random Forest</td><td>随机森林</td><td>多棵决策树投票的集成方法</td></tr>
<tr><td>SVM / SVC</td><td>支持向量机/分类器</td><td>最大化类别间隔的分类器</td></tr>
<tr><td>XGBoost</td><td>极端梯度提升</td><td>Sequential boosting 的集成方法</td></tr>
<tr><td>Train/Test Split</td><td>训练/测试集划分</td><td>留出法验证</td></tr>
<tr><td>Stratified Split</td><td>分层划分</td><td>保持正负比例一致的划分</td></tr>
<tr><td>Scaffold Split</td><td>骨架划分</td><td>按分子骨架分组的验证方式</td></tr>
<tr><td>Overfitting</td><td>过拟合</td><td>训练集学得好但泛化差</td></tr>
<tr><td>Generalization</td><td>泛化</td><td>模型在未见数据上的表现</td></tr>
<tr><td>Accuracy</td><td>准确率</td><td>(TP+TN)/total</td></tr>
<tr><td>Precision</td><td>精确率/查准率</td><td>TP/(TP+FP)</td></tr>
<tr><td>Recall / Sensitivity</td><td>召回率/查全率</td><td>TP/(TP+FN)</td></tr>
<tr><td>F1 Score</td><td>F1分数</td><td>Precision和Recall的调和平均</td></tr>
<tr><td>ROC-AUC</td><td>ROC曲线下面积</td><td>模型整体区分能力的度量</td></tr>
<tr><td>Confusion Matrix</td><td>混淆矩阵</td><td>TP/TN/FP/FN的四象限表</td></tr>
<tr><td>False Positive (FP)</td><td>假阳性/I类错误</td><td>实际非活性被预测为活性</td></tr>
<tr><td>False Negative (FN)</td><td>假阴性/II类错误</td><td>实际活性被预测为非活性</td></tr>
<tr><td>Feature Importance</td><td>特征重要性</td><td>特征对预测的贡献程度</td></tr>
<tr><td>Cross-Validation</td><td>交叉验证</td><td>K折验证，更稳健的评估</td></tr>
</table>

<h3>Pharmacy / Binding</h3>
<table>
<tr><th>英文</th><th>中文</th><th>说明</th></tr>
<tr><td>EGFR</td><td>表皮生长因子受体</td><td>Epidermal Growth Factor Receptor</td></tr>
<tr><td>ATP-binding pocket</td><td>ATP结合口袋</td><td>激酶的催化位点，抑制剂靶标</td></tr>
<tr><td>Hinge region</td><td>铰链区</td><td>激酶N端和C端连接处，形成关键氢键</td></tr>
<tr><td>DFG motif</td><td>DFG基序</td><td>Asp-Phe-Gly序列，激酶活性调控关键</td></tr>
<tr><td>Type 1 / Type 2 inhibitor</td><td>I型/II型抑制剂</td><td>活性/非活性构象结合的抑制剂</td></tr>
<tr><td>Privileged scaffold</td><td>优势骨架</td><td>对某靶点家族反复出现活性的骨架</td></tr>
<tr><td>Lipinski's Rule of Five</td><td>类药五规则</td><td>MW<500, LogP<5, HBD<5, HBA<10</td></tr>
<tr><td>Veber's Rules</td><td>Veber规则</td><td>RotBonds<10, TPSA<140 for oral bioavailability</td></tr>
<tr><td>Oral bioavailability</td><td>口服生物利用度</td><td>药物口服后的吸收程度</td></tr>
<tr><td>Membrane permeability</td><td>膜透性</td><td>分子穿过细胞膜的能力</td></tr>
<tr><td>Inductive bias</td><td>归纳偏置</td><td>模型的内置假设，影响泛化</td></tr>
<tr><td>Virtual screening</td><td>虚拟筛选</td><td>用模型从大规模化合物库筛选候选</td></tr>
</table>
</div>

<!-- ==================== 项目反思 ==================== -->

<h2>项目反思</h2>

<div class="card">
<div class="card-title">Limitations & Lessons</div>

<h3>不足之处</h3>
<ul>
<li><strong>互变异构统一丢失信息</strong>：不同互变异构体确实有不同性质（指纹、疏水性、pKa），标准化统一是为了去重的妥协，不是因为没有影响</li>
<li><strong>描述符太少</strong>：7 个理化描述符远不足以区分活性/非活性，2048 维指纹才是主力</li>
<li><strong>模型未调参</strong>：所有模型用默认参数，XGBoost 调参后可能反超 SVM</li>
<li><strong>骨架划分的正负比例未检查</strong>：SVM+指纹的骨架划分 F1 异常高于随机划分，可能是测试集正负比例偏斜</li>
<li><strong>未做比特解码</strong>：指纹 Top 20 重要比特的化学意义未还原</li>
</ul>

<h3>经验总结</h3>
<ul>
<li>数据清洗是"对错问题"（空值、重复、格式），异常值过滤是"范围问题"（取决于研究目标），两者不同层面</li>
<li>骨架划分是药物 QSAR 的标准做法，随机划分会高估模型性能</li>
<li>模型选型取决于数据特征：高维稀疏 → SVM 强；低维稠密 → RF/XGB 更合适</li>
<li>特征重要性不等于因果性：HBD 排名最低不意味着不重要，可能是因为同靶点内变化太小</li>
<li>系统思维 > 单步优化：数据质量 → 特征表征 → 模型选择 → 验证方式，每个环节的选择都隐含假设，整体表现取决于假设是否自洽</li>
</ul>
</div>

<!-- ==================== 下一步 ==================== -->

<h2>下一步方向</h2>

<div class="card">
<div class="card-title">Next Steps</div>
<ol>
<li><strong>调参优化</strong>：用 GridSearchCV 或 Optuna 给 XGBoost 调参，看能否超过 SVM</li>
<li><strong>比特解码</strong>：把重要的 Morgan 指纹比特还原成子结构，看看到底是什么基团</li>
<li><strong>更多描述符</strong>：加入 EState、VSA、 pharmacophore 等描述符，看区分度是否提升</li>
<li><strong>其他靶点</strong>：同样的流程跑 COX-2 或 CDK2，对比不同靶点的模型差异</li>
<li><strong>读文献</strong>：读 1-2 篇 EGFR QSAR 论文，对比自己的结果与文献的差异</li>
</ol>
</div>

<div class="footer">
EGFR QSAR Project · 2026.09–2026.10 · AIDD Learning Series
</div>

</body>
</html>
    """

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'\n总结报告已保存到：{report_path}')
    print(f'\n项目完成！')
    print(f'  数据：5000 → 2030 个唯一分子')
    print(f'  模型：18种组合，最佳 SVM+指纹 F1=0.912')
    print(f'  图表：12张（ROC、混淆矩阵、特征重要性、分布图）')
    print(f'  报告：HTML 总结报告')


if __name__ == '__main__':
    main()
