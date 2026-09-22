"""
模型评估模块
"""
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def evaluate_regression(y_true, y_pred, verbose= True):
   mse = mean_squared_error(y_true, y_pred)
   rmse = np.sqrt(mse)
   r2 = r2_score(y_true, y_pred)
   mae = mean_absolute_error(y_true, y_pred)

   if verbose:
      print ( f"MSE: {mse: .3 f} " ) 
      print ( f"RMSE: {rmse: .3 f} " ) 
      print ( f"MAE: {mae: .3 f} " ) 
      print ( f"R²: {r2: .3 f} " )

   return {'mse' : mse, 'rmse' : rmse, 'r2' : r2, 'mae' : mae }
