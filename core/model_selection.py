import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")

def suggest_best_model(df):
    """
    Compare ARIMA and Prophet on MAPE with enhanced validation
    """
    MIN_DATA_POINTS = 6  # Minimum required for modeling
    
    # Validate input
    if df.empty or 'demand' not in df.columns:
        return "No valid demand data"
    
    # Clean dates and demand
    clean_df = df.dropna(subset=['date', 'demand']).copy()
    clean_df['date'] = pd.to_datetime(clean_df['date'], errors='coerce')
    clean_df = clean_df.dropna(subset=['date'])
    
    # Check data sufficiency
    if len(clean_df) < MIN_DATA_POINTS:
        return f"Need {MIN_DATA_POINTS}+ points (has {len(clean_df)})"
    
    # Prepare series
    clean_df = clean_df.sort_values('date')
    y = clean_df['demand'].values
    mape_scores = {}

    # ARIMA
    try:
        model_arima = ARIMA(y, order=(2, 1, 2)).fit()
        forecast_arima = model_arima.forecast(steps=len(y))
        mape_scores['ARIMA'] = mean_absolute_percentage_error(y, forecast_arima)
    except Exception as e:
        mape_scores['ARIMA'] = float('inf')

    # Prophet
    try:
        prophet_df = clean_df.rename(columns={'date': 'ds', 'demand': 'y'})
        model_prophet = Prophet()
        model_prophet.fit(prophet_df)
        future = model_prophet.make_future_dataframe(periods=0)
        forecast_prophet = model_prophet.predict(future)
        mape_scores['Prophet'] = mean_absolute_percentage_error(
            clean_df['y'], forecast_prophet['yhat'][:len(clean_df)]
        )
    except Exception as e:
        mape_scores['Prophet'] = float('inf')

    return min(mape_scores, key=mape_scores.get)