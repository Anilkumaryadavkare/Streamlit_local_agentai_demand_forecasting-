import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")

def suggest_best_model(df):
    """
    Compare ARIMA and Prophet on MAPE and return the better one.
    
    Args:
        df (pd.DataFrame): Time series data with 'date' and 'demand' columns.
    
    Returns:
        str: The name of the best model based on MAPE.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    y = df['demand'].values
    mape_scores = {}

    # ARIMA
    try:
        model_arima = ARIMA(y, order=(2, 1, 2)).fit()
        forecast_arima = model_arima.forecast(steps=len(y))
        mape_scores['ARIMA'] = mean_absolute_percentage_error(y, forecast_arima)
    except Exception:
        mape_scores['ARIMA'] = float('inf')

    # Prophet
    try:
        prophet_df = df.rename(columns={'date': 'ds', 'demand': 'y'})
        model_prophet = Prophet()
        model_prophet.fit(prophet_df)
        future = model_prophet.make_future_dataframe(periods=0)
        forecast_prophet = model_prophet.predict(future)
        mape_scores['Prophet'] = mean_absolute_percentage_error(
            df['demand'], forecast_prophet['yhat'][:len(df)]
        )
    except Exception:
        mape_scores['Prophet'] = float('inf')

    best_model = min(mape_scores, key=mape_scores.get)
    return best_model
