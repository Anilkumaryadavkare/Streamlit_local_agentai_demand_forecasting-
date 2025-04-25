import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_forecast(segments, model_map=None):
    """
    Generate forecasts for each cluster using a simple rolling average.
    
    Args:
        segments (dict): A dictionary with cluster IDs as keys and DataFrames as values.
        model_map (dict): Optional dict mapping cluster IDs to model names (not used in this MVP).
    
    Returns:
        pd.DataFrame: Combined forecasted DataFrame.
    """
    forecast_dfs = []

    for cluster_id, df in segments.items():
        if 'demand' not in df.columns:
            print(f"[!] Cluster {cluster_id} missing 'demand'. Skipping.")
            continue

        df = df.copy()
        df = df.sort_values("date")
        df['forecast'] = df['demand'].rolling(window=3).mean().bfill()
        forecast_dfs.append(df)

    if not forecast_dfs:
        raise ValueError("No valid clusters found.")

    combined_forecast_df = pd.concat(forecast_dfs, ignore_index=True)
    print("[✔] Forecasts created using simple rolling average.")
    return combined_forecast_df


def create_side_by_side_chart(df):
    """
    Create a side-by-side Plotly chart of actual vs forecasted demand.
    
    Args:
        df (pd.DataFrame): Must contain 'date', 'demand', 'forecast'.
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Actual Demand", "Forecasted Demand"))

    fig.add_trace(
        go.Scatter(x=df['date'], y=df['demand'], mode='lines+markers', name='Actual'),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df['date'], y=df['forecast'], mode='lines+markers', name='Forecast'),
        row=1, col=2
    )

    fig.update_layout(
        title="Actual vs Forecasted Demand",
        height=500,
        width=1000
    )
    return fig
