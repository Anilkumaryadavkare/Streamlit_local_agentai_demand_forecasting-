import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_forecast(segments, model_map, forecast_periods=4):
    """
    Generate past and future forecasts with clear labeling
    """
    forecast_dfs = []
    for cluster_id, df in segments.items():
        # Add model tracking
        model_name = model_map.get(cluster_id, "Prophet")
        df['model'] = model_name
        df['cluster'] = cluster_id
    for segment_key, df in segments.items():
        if 'date' not in df.columns or 'demand' not in df.columns:
            continue
        
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date']).sort_values('date')

        if df.empty:
            continue

        # Historical forecast (simple moving average)
        df['forecast'] = df['demand'].rolling(window=3).mean().bfill()
        df['forecast_type'] = 'Past Forecast'
        df['Segment'] = segment_key

        # Future forecast
        last_date = df['date'].max()
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=forecast_periods,
            freq='MS'
        )

        future_df = pd.DataFrame({
            'date': future_dates,
            'forecast': df['forecast'].iloc[-1],  # Flat projection
            'forecast_type': 'Future Forecast',
            'Segment': segment_key
        })

        forecast_dfs.append(pd.concat([df, future_df], ignore_index=True))
    return pd.concat(forecast_dfs)
    combined = pd.concat(forecast_dfs, ignore_index=True)
    print(f"[✔] Generated {forecast_periods} period future forecast")
    return combined

def create_side_by_side_chart(df):
    """Professional timeline visualization"""
    fig = go.Figure()

    # Actual Demand
    if 'demand' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['demand'],
            mode='lines+markers',
            name='Actual Demand',
            line=dict(color='#1f77b4', width=3)
        ))

    # Past Forecast
    past = df[df['forecast_type'] == 'Past Forecast']
    fig.add_trace(go.Scatter(
        x=past['date'],
        y=past['forecast'],
        mode='lines+markers',
        name='Past Forecast (Validation)',
        line=dict(color='#ff7f0e', dash='dash', width=2)
    ))

    # Future Forecast
    future = df[df['forecast_type'] == 'Future Forecast']
    fig.add_trace(go.Scatter(
        x=future['date'],
        y=future['forecast'],
        mode='lines+markers',
        name='Next 6-Month Forecast',
        line=dict(color='#2ca02c', width=4),
        fill='tozeroy'
    ))

    fig.update_layout(
        title="Demand Forecast Timeline",
        xaxis_title="Timeline",
        yaxis_title="Units",
        template="plotly_white",
        hovermode="x unified",
        height=600
    )
    return fig
