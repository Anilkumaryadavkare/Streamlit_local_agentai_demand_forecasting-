import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np

def evaluate_forecast_models(forecast_df):
    """Evaluate models using lowercase column names"""
    metrics = []
    
    # Group by cluster and model
    for (cluster, model), group in forecast_df.groupby(["cluster", "model"]):
        try:
            y_true = group['demand'].dropna()
            y_pred = group['forecast'].dropna()
            
            if len(y_true) == 0 or len(y_pred) == 0:
                continue
                
            metrics.append({
                "cluster": cluster,
                "model": model,
                "mape": mean_absolute_percentage_error(y_true, y_pred) * 100,
                "rmse": np.sqrt(mean_squared_error(y_true, y_pred))
            })
        except Exception as e:
            continue
            
    return pd.DataFrame(metrics)