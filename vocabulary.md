# AIDD 学习常用词汇

## Python 基础

| 英文 | 中文 | 说明 |
|---|---|---|
| variable | 变量 | `name = 'aspirin'` |
| assign | 赋值 | `=` 就是赋值 |
| loop | 循环 | `for name in items:` |
| iterate | 遍历 | 循环过一遍列表 |
| append | 追加 | `list.append(...)` 往尾部加 |
| index | 索引 | `c[0]` 取第一个 |
| slice | 切片 | `list[1:5]` 取第2到第4个 |
| nested | 嵌套 | for 里面再套 for |
| break | 跳出 | 打断循环 |
| continue | 继续 | 跳过本次，回到循环开头 |
| exception | 异常 | 程序运行时的错误 |
| raise | 抛出 | 主动产生一个错误 |
| catch | 捕获 | except 接住错误 |
| argument | 参数（传入值） | 调用函数时传的值 |
| parameter | 参数（定义值） | 函数定义里的变量 |
| return | 返回 | 函数给回来的结果 |
| call | 调用 | 执行一个函数 |
| import | 导入 | 引入外部库 |
| module | 模块 | 一个 .py 文件 |
| function | 函数 | `def` 定义的 |
| scope | 作用域 | 变量在哪里能被访问 |

## 数据结构

| 英文 | 中文 | 说明 |
|---|---|---|
| list | 列表 | `[1, 2, 3]` |
| dict | 字典 | `{'aspirin': 'CC(=O)O...'}` |
| tuple | 元组 | `(name, smiles)` 不可改 |
| key | 键 | 字典里的名字部分 |
| value | 值 | 字典里键对应的内容 |
| item | 项 | 字典里的一对 key-value |
| array | 数组 | NumPy 的 `np.array()` |
| shape | 形状 | 数组维度 `(100, 7)` |
| empty | 空 | `[]` 或 `{}` |

## RDKit / 化学信息学

| 英文 | 中文 | 说明 |
|---|---|---|
| SMILES | 分子线性表达式 | 用文本表示分子结构 |
| mol / molecule | 分子对象 | RDKit 解析后的分子 |
| descriptor | 描述符 | 分子的数值特征（MW、LogP等） |
| parse | 解析 | 文本 → 程序能处理的对象 |
| valid / invalid | 有效 / 无效 | SMILES 能不能被解析 |
| canonical | 规范的 | 标准形式的 SMILES |
| aromatic | 芳香的 | 苯环等芳香结构 |
| saturated | 饱和的 | 没有双键/三键 |
| ring | 环 | 环状结构 |
| bond | 键 | 原子之间的连接 |
| atom | 原子 | 分子里的原子 |
| heavy atom | 重原子 | 非氢原子 |
| charge | 电荷 | 分子的形式电荷 |

## 机器学习

| 英文 | 中文 | 说明 |
|---|---|---|
| feature | 特征 | 输入变量（描述符） |
| label | 标签 | 输出/目标值 |
| train | 训练 | 让模型学 |
| predict | 预测 | 模型给结果 |
| fit | 拟合 | 模型学数据的过程 |
| score | 得分 | 模型表现分数 |
| accuracy | 准确率 | 预测对了的比例 |
| classifier | 分类器 | 分类的模型 |
| regressor | 回归器 | 预测连续值的模型 |
| split | 分割 | 划分训练/测试集 |
| cross validation | 交叉验证 | 多次验证取平均 |
| overfitting | 过拟合 | 模型死记硬背，泛化差 |
| importance | 重要性 | 特征对模型的贡献 |
| estimator | 估计器 | sklearn 里模型的统称 |

## 工程

| 英文 | 中文 | 说明 |
|---|---|---|
| script | 脚本 | 一个 .py 文件 |
| run | 运行 | 执行脚本 |
| debug | 调试 | 找错 |
| error | 错误 | 程序出问题 |
| warning | 警告 | 不致命但要注意 |
| comment | 注释 | `#` 后面的说明 |
| constant | 常量 | 不变的值 |
| threshold | 阈值 | 判断标准值（如 500） |
| validate | 校验 | 检查数据是否合理 |
| cache | 缓存 | 存中间结果复用 |
