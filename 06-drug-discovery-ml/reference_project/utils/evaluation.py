"""
模型评估模块 - 参考实现
"""
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
# metrics(评估指标)模块导入三个回归模型评估指标，mean_squared_error（MSE，均方误差），r2_score（R²，决定系数），mean_absolute_error（MAE，平均绝对误差）


def evaluate_regression(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)     #sqrt平方根，开平方
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    #作用是将四个指标打包成一个字典返回，左边的是键，右边是值，用字典的好处是按名字取清晰
    return {'mse': mse, 'rmse': rmse, 'mae': mae, 'r2': r2}
