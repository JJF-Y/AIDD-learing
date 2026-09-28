# 概念笔记

> 每个概念一篇完整讲解，按主题分类，底部附相关概念链接，形成网状知识结构。

---

## 概念地图

```mermaid
graph TD
    %% 分子表示
    A[分子表示] --> B[理化描述符<br>MW、LogP、HBA 等]
    A --> C[Morgan 指纹<br>morgan_fingerprint]
    C --> C1[radius 半径]
    C --> C2[n_bits 位数]
    C --> C3[ConvertToNumpyArray]

    %% 模型
    D[机器学习模型] --> E[RandomForest]
    D --> F[XGBoost<br>xgb_parameters]
    D --> G[SVR]

    %% XGBoost 细节
    F --> F1[learning_rate 学习率]
    F --> F2[n_estimators 树数量]
    F --> F3[max_depth 树深度]
    F --> F4[subsample 子采样]
    F --> F5[colsample 列采样]
    F --> F6[early_stopping 早停<br>early_stopping]

    %% 评估与验证
    H[模型评估] --> H1[交叉验证<br>cross_validation]
    H --> H2[评估指标<br>MSE / RMSE / MAE / R²]
    H --> H3[训练集 / 验证集 / 测试集]

    %% 过拟合
    I[过拟合] --> F6
    I --> F4
    I --> F5

    %% 关系连线
    F1 -.-> F2
    F6 -.-> H3
    C3 -.-> F

    style A fill:#f9f,stroke:#333
    style D fill:#9f9,stroke:#333
    style H fill:#ff9,stroke:#333
    style I fill:#f99,stroke:#333
```

> 粉色：分子表示 | 绿色：模型 | 黄色：评估 | 红色：核心问题

---

## 按主题分类

### 分子表示

| 概念 | 一句话 |
|------|--------|
| [Morgan 分子指纹](morgan_fingerprint.md) | 把分子结构编码成 0/1 数组，用于机器学习 |

### 模型与调参

| 概念 | 一句话 |
|------|--------|
| [XGBoost 参数详解](xgb_parameters.md) | 每个参数调大调小的影响、参数间互相关系、调参顺序 |
| [早停机制](early_stopping.md) | 监控验证集性能，连续 N 轮没提升就停，防止过拟合 |

---

## 阅读路径建议

按从基础到进阶的顺序：

```
分子描述符 → Morgan 指纹
                ↓
          机器学习基础 → 交叉验证
                ↓
          XGBoost 参数 → 早停机制
```

---

## 说明

- 每个概念笔记底部都有"相关概念"链接，可跳转阅读
- 概念图持续更新，学到新概念往里加
- 文件名即主题，英文小写，下划线分隔
