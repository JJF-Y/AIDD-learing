"""
模型训练与交叉验证模块 - 参考实现
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score


def train_regression_model(X_train, y_train, model_type='rf', **kwargs):
    if model_type == 'rf':
        n_est = kwargs.get('n_estimators', 200)
        rs = kwargs.get('random_state', 42)
        model = RandomForestRegressor(n_estimators=n_est, random_state=rs)
    elif model_type == 'svr':
        kernel = kwargs.get('kernel', 'rbf')
        model = SVR(kernel=kernel)
    elif model_type == 'xgb':
        try:
            from xgboost import XGBRegressor
            rs = kwargs.get('random_state', 42)
            model = XGBRegressor(random_state=rs)
        except ImportError:
            raise ImportError('请先安装xgboost: pip install xgboost')
    else:
        raise ValueError(f'不支持的模型类型: {model_type}')
    model.fit(X_train, y_train)
    return model


def cross_validate(X, y, model_type='rf', cv=5, scoring='r2', **kwargs):
    if model_type == 'rf':
        n_est = kwargs.get('n_estimators', 200)
        rs = kwargs.get('random_state', 42)
        model = RandomForestRegressor(n_estimators=n_est, random_state=rs)
    elif model_type == 'svr':
        kernel = kwargs.get('kernel', 'rbf')
        model = SVR(kernel=kernel)
    elif model_type == 'xgb':
        try:
            from xgboost import XGBRegressor
            rs = kwargs.get('random_state', 42)
            model = XGBRegressor(random_state=rs)
        except ImportError:
            raise ImportError('请先安装xgboost: pip install xgboost')
    else:
        raise ValueError(f'不支持的模型类型: {model_type}')
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    return scores
