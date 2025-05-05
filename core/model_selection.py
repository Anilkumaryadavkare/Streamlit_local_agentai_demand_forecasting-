import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings

warnings.filterwarnings("ignore")

def rolling_forecast(y, window=3):
    return pd.Series(y).rolling(window=window, min_periods=1).mean().shift(1).fillna(method='bfill').values

def suggest_best_model(df):
    """
    Compare ARIMA, Prophet, Rolling Average, and Exponential Smoothing on MAPE
    """
    MIN_DATA_POINTS = 6

    if df.empty or 'demand' not in df.columns:
        return "No valid demand data"

    clean_df = df.dropna(subset=['date', 'demand']).copy()
    clean_df['date'] = pd.to_datetime(clean_df['date'], errors='coerce')
    clean_df = clean_df.dropna(subset=['date'])

    if len(clean_df) < MIN_DATA_POINTS:
        return f"Need {MIN_DATA_POINTS}+ points (has {len(clean_df)})"

    clean_df = clean_df.sort_values('date')
    y = clean_df['demand'].values
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
        prophet_df = clean_df.rename(columns={'date': 'ds', 'demand': 'y'})
        model_prophet = Prophet()
        model_prophet.fit(prophet_df)
        future = model_prophet.make_future_dataframe(periods=0)
        forecast_prophet = model_prophet.predict(future)
        mape_scores['Prophet'] = mean_absolute_percentage_error(
            clean_df['demand'].values, forecast_prophet['yhat'][:len(clean_df)].values
        )
    except Exception:
        mape_scores['Prophet'] = float('inf')

    # Rolling Average
    try:
        forecast_rolling = rolling_forecast(y)
        mape_scores['RollingAverage'] = mean_absolute_percentage_error(y, forecast_rolling)
    except Exception:
        mape_scores['RollingAverage'] = float('inf')

    # Exponential Smoothing
    try:
        model_ets = ExponentialSmoothing(y, trend='add', seasonal=None).fit()
        forecast_ets = model_ets.fittedvalues
        mape_scores['ExpSmoothing'] = mean_absolute_percentage_error(y, forecast_ets)
    except Exception:
        mape_scores['ExpSmoothing'] = float('inf')

    return min(mape_scores, key=mape_scores.get)
