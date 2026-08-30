import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_squared_error, r2_score)

from rdkit import Chem
from rdkit.Chem import Descriptors

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


drug_smiles = {                                                         #样本数据
    'aspirin':     'CC(=O)OC1=CC=CC=C1C(=O)O',
    'caffeine':    'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
    'paracetamol': 'CC(=O)NC1=CC=C(O)C=C1',
    'ibuprofen':   'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O',
    'naproxen':    'CC(=O)OC1=CC=C(C=C1)C2=CC=CC=C2',
    'metformin':   'CN(C)C(=N)N=C(N)N',
    'warfarin':    'CC(=O)CC(C1=CC=CC=C1)C2=C(C3=CC=CC=C3OC2=O)O',
    'diclofenac':  'C1=CC=C(C=C1)NCC2=CC=C(C=C2)Cl',
    'omeprazole':  'COc1ccc2[nH]c(nc2c1)S(=O)Cc1ncc(C)c(OC)c1C',
    'simvastatin': 'CC(C)C1C(C(C(=O)O1)C)C2C3CC=C(CCC3(C)C2O)C',
    '大分子A':      'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
    '大分子B':      'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
    '大分子C':      'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
}


def calc_descriptors(smiles):   #自定义函数
    mol = Chem.MolFromSmiles(smiles)    #将smiles分子转变为分子对象
    if mol is None: #避免因为某个转换失败导致，接下来无法进行
        return None     #返回输出None
    return [Descriptors.MolWt(mol), Descriptors.MolLogP(mol),
            Descriptors.NumHAcceptors(mol), Descriptors.NumHDonors(mol)]    #Descriptors是模块，这里是调用四个描述符函数


def check_lipinski(smiles): #自定义函数
    mol = Chem.MolFromSmiles(smiles)    #同上，虽然是一样的，但是因为是内置在自定义函数里的，所以单独
    if mol is None:
        return -1, 'SMILES 解析失败'
    mw   = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hba  = Descriptors.NumHAcceptors(mol)
    hbd  = Descriptors.NumHDonors(mol)
    violations = 0  #violations是个计数器,这一步是设定初始值
    if mw > 500:   violations += 1  #if判断，用初步简单判断
    if logp > 5:   violations += 1
    if hba > 10:   violations += 1
    if hbd > 5:    violations += 1
    return violations, f'MW={mw:.1f}, LogP={logp:.2f}, HBA={hba}, HBD={hbd}'    #返回值，输出

#三个空列表
features = []
labels = []
names = []

for name, smiles in drug_smiles.items():    #item循环遍历，因为drug_smiles里是二元元组，相当于将元组拆解，一一分配，一次一个
    mol = Chem.MolFromSmiles(smiles)    #将smiles分子转变为分子对象
    if mol is None:
        print(f'{name} 解析失败，跳过')
        continue    #返回
    #调用的四个描述符函数
    mw   = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hba  = Descriptors.NumHAcceptors(mol)
    hbd  = Descriptors.NumHDonors(mol)
    features.append([mw, logp, hba, hbd])   #将上述四个模块的输出整合为列表添加给features列表
    names.append(name)  #name添加给names列表
    violations = 0  #依旧计数器
    if mw > 500:   violations += 1
    if logp > 5:   violations += 1
    if hba > 10:   violations += 1
    if hbd > 5:    violations += 1
    labels.append(1 if violations <= 1 else 0)  #还是给列表添加，这个有运算式

X = np.array(features)  #将features列表转变为numpy数组，改成 转为 numpy 数组，方便切片和矩阵运算
y = np.array(labels)    #同理，但是要注意X是大写,y是小写，书写习惯，用以区分，二维数组和一维向量，一维向量支持运算，诸如加减乘除

print(f'样本数: {len(names)}，合格: {y.sum()}，不合格: {len(y) - y.sum()}')
#len(names)输出的是names列表中的元素个数，y.sum()是计算总和，因为合格的为1，不合格的为0，len(y) - y.sum()相当于用总数减去合格的

#enumerate循环函数,会给每个值添加一个序号，i就是那个承接序号的变量
for i, name in enumerate(names):
    print(f'  {name:15s} MW={X[i][0]:7.1f} LogP={X[i][1]:6.2f} '
          f'HBA={X[i][2]:2.0f} HBD={X[i][3]:2.0f} → {"合格" if y[i]==1 else "不合格"}')
    #同上


fig, ax = plt.subplots(figsize=(10, 4)) #生成画布，figsize=(10, 4)画布大小
colors = ['#4B3FE3' if l == 1 else '#E8463A' for l in y]    #设置颜色，l遍历y，结合判断式，给予不同的颜色
bars = ax.bar(names, X[:, 0], color=colors, alpha=0.8)  #生成柱状图，依次是名字，分子量数据，颜色，透明度，越大越深
ax.set_title('各药物分子量', fontsize=14)   #设置总标题
ax.set_ylabel('Da', fontsize=12)    #设置y轴标题
ax.tick_params(axis='x', rotation=45)   #这个可能是让X轴的字倾斜45度
for bar, value in zip(bars, X[:, 0]):   #给柱子上数据
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{value:.0f}', ha='center', va='bottom', fontsize=8)
#ax.text前面是确定位置的，bar.get_x() + bar.get_width()/2柱子水平中心的位置，bar.get_height() + 5柱子顶部高度加5（避免数据与柱子重合）
#f'{value:.0f}'不保留小数，ha='center'水平居中对齐，va='bottom'底部对齐

plt.tight_layout()
plt.savefig('drug_mw.png', dpi=150, bbox_inches='tight')    #名字加格式，分辨率，紧凑裁剪，去掉图周围多余的空白
plt.show()  #展示

fig, ax = plt.subplots(figsize=(8, 5))  #设置画布
for cls, color, label in [(1, '#4B3FE3', '合格'), (0, '#E8463A', '不合格')]:    #相当于给三元组解包，依次赋值,有两个列表，所以需要循环两次，第一次合格的，第二次不合格的
    mask = y == cls #生成布尔掩码，生成布尔数组，若为真则输出True，若为假则输出False,就是前后这个是否成立相同
    ax.scatter(X[mask, 0], X[mask, 1], s=120, c=color,  #生成散点图，这里的坐标是由X列表提供的，依次是取结果为True的第一列和第二列分别做点的X轴坐标和Y轴的坐标，
               #关于这个mask，就是mask 为 True 的行，那么怎么实现先是合格后是不合格的呢，就是靠mask = y == cls，两次循环，cls的值都是不同的，所以两次循环True值的位置也都不相同
               edgecolors='white', linewidth=1.5, label=label, zorder=3)    #edgecolors='white'点的边缘为白色，linewidth=1.5边缘的宽度，label=label图例名称，zorder=3层级，高层级可以覆盖底层级
for i, name in enumerate(names):
    ax.annotate(name, (X[i][0], X[i][1]),   #X[i][0], X[i][1]),相当于提供坐标告诉名字要往哪里加
                textcoords='offset points', xytext=(5, 5), fontsize=9)  
    #textcoords='offset points'设置偏移量单位，而这个的意义是为了后面的服务告诉后面那个用什么单位这个5是多大，xytext=(5, 5)文字相对锚点的偏移量

ax.set_title('分子量 vs LogP', fontsize=14)
ax.set_xlabel('分子量 (Da)', fontsize=12)
ax.set_ylabel('LogP', fontsize=12)
ax.legend(fontsize=11)  #显示图例
ax.grid(True, alpha=0.3, linestyle='--')    #开启网格线，透明度，形式风格
plt.tight_layout()
plt.savefig('mw_vs_logp.png', dpi=150, bbox_inches='tight')
plt.show()

feature_labels = ['分子量 (Da)', 'LogP', '氢键受体数', '氢键供体数']    #自己的定义的一个列表
fig, axes = plt.subplots(2, 2, figsize=(12, 8)) #生成2×2子图，总画布大小为(12,8)，输出返回的矩阵2行2列

#这个比较复杂，先是axes.flat，将矩阵拉平转变为一维，然后zip循环依次配对，打包成二元元组，然后再由enumerate循环添加序号并配对，
# 因为配对对应的二元元组有两个元素，所以对应的有两个变量接收，同时因为是接收元组所以形式上也要符合所以是()
for i, (ax, label) in enumerate(zip(axes.flat, feature_labels)):
    for cls, color in [(1, '#4B3FE3'), (0, '#E8463A')]:
        mask = y == cls
        ax.hist(X[mask, i], bins=8, alpha=0.6, color=color,
                label='合格' if cls == 1 else '不合格')
    ax.set_title(label, fontsize=12)
    ax.legend(fontsize=9)
plt.suptitle('特征分布：合格 vs 不合格', fontsize=14, y=0.95)   #总标题，y=0.95，是总标题的相对于整个画布的高度
plt.tight_layout()
plt.savefig('feature_distribution.png', dpi=150, bbox_inches='tight')
plt.show()


X_train, X_test, y_train, y_test = train_test_split(    #划分数据集，
    X, y, test_size=0.3, random_state=42, stratify=y    #stratify=y保证训练集和测试集里，合格/不合格的比例和原始数据一样。
)

clf_model = RandomForestClassifier(random_state=42, n_estimators=100)   #创建模型，n_estimators=100树的数量
clf_model.fit(X_train, y_train) #训练模型
y_pred = clf_model.predict(X_test)  #分类模型对预测集数据进行预测

print(f'\n训练集: {len(X_train)}，测试集: {len(X_test)}')
print(f'准确率: {accuracy_score(y_test, y_pred):.2f}')  #计算准确率，y_test真实数据，y_pred预测标签

print('\n分类报告:')
print(classification_report(y_test, y_pred, #classification_report，一键生成所有指标的工具
                           labels=[0, 1],   #避免因为出现全对或者全错的情况导致有的结果没有显示进而导致报错
                           target_names=['不合格', '合格'], #把0和1替换为不合格和合格
                           zero_division=0))    #某一类算不出指标时（比如除以零），显示 0 而不是报错

cm = confusion_matrix(y_test, y_pred, labels=[0, 1])    #生成混淆矩阵，一个2×2的表格
print(cm)
print('混淆矩阵:')
print(f'  真实\\预测  不合格  合格')
print(f'  不合格     {cm[0][0]:6d}  {cm[0][1]:4d}')
print(f'  合格       {cm[1][0]:6d}  {cm[1][1]:4d}')

scores = cross_val_score(clf_model, X, y, cv=5)     #交叉验证，用什么模型，全部的特征数据，全部的标签，5 折交叉验证，数据切 5 份，每份轮流做测试集，返回 5 个准确率
print(f'\n5折交叉验证: {scores}')
print(f'平均: {scores.mean():.2f} ± {scores.std():.2f}')    #std标准差，越小越稳定

feature_names = ['分子量', 'LogP', '氢键受体数', '氢键供体数']  #创建列表
importances = clf_model.feature_importances_    #输出各个特征的重要程度占比
print('\n特征重要性:')
for name, imp in zip(feature_names, importances):   #zip循环一一配对
    print(f'  {name:10s}: {imp:.4f}')   #name字符串长度10个，imp即重要程度占比保留小数点后四位

fig, ax = plt.subplots(figsize=(8, 4))  #设置画板
ax.bar(feature_names, importances, color='#4B3FE3', alpha=0.8)      #柱状图
ax.set_title('特征重要性', fontsize=14) #总标题
ax.set_ylabel('重要性', fontsize=12)    #Y轴标题
for i, v in enumerate(importances): #enumerate循环
    ax.text(i, v + 0.01, f'{v:.3f}', ha='center', fontsize=10)  #i第几个柱子，v + 0.01在柱子高度加0.01避免文字与柱子重合，f'{v:.3f}'保留小数点后三位，ha='center'正上方居中
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
plt.show()


new_smiles = 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O'    #定义一个新分子
new_mol = Chem.MolFromSmiles(new_smiles)    #Smile式转变为分子对象
new_features = [[Descriptors.MolWt(new_mol), Descriptors.MolLogP(new_mol),
                 Descriptors.NumHAcceptors(new_mol), Descriptors.NumHDonors(new_mol)]]
prediction = clf_model.predict(new_features)    #预测新分子，输出分类结果
probability = clf_model.predict_proba(new_features)     #同上，但是输出的是概率

print(f'\n预测新分子: {new_smiles}')
print(f'  MW={new_features[0][0]:.1f} LogP={new_features[0][1]:.2f} '   #目的就按顺序输出新分子的四个特征
      f'HBA={new_features[0][2]:.0f} HBD={new_features[0][3]:.0f}')
print(f'  结果: {"合格" if prediction[0]==1 else "不合格"}')
if probability.shape[1] > 1:        #probability.shape[1] 查看概率数组的列数
    print(f'  合格概率: {probability[0][1]:.1%}')
else:
    print(f'  合格概率: {probability[0][0]:.1%}（模型只见过合格类）')


np.random.seed(42)  #固定随机种子，保证结果可复现
X_reg = np.random.normal(300, 100, (50, 4))     #从正态分布随机取值，均值300，标准差100，，形状是50行4列
y_reg = X_reg[:, 0] * 0.01 + X_reg[:, 1] * 0.5 + np.random.normal(0, 0.5, 50)

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(    #划分数据集，一部分做训练集，一部分做测试集，random_state=42作用依然是保证结果可以复现
    X_reg, y_reg, test_size=0.3, random_state=42
)

reg_model = RandomForestRegressor(random_state=42, n_estimators=100)    #创建随机森林回归模型，后面还需要训练
reg_model.fit(X_train_r, y_train_r)     #训练模型
y_pred_r = reg_model.predict(X_test_r)     #验证

print(f'\n回归模型:')
print(f'  MSE: {mean_squared_error(y_test_r, y_pred_r):.4f}')   #均方误差
print(f'  R²:  {r2_score(y_test_r, y_pred_r):.4f}')     #决定系数