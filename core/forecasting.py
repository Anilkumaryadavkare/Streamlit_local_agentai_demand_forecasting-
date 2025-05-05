# forecasting.py

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def generate_forecast(segments, model_map, forecast_periods=4):
    """
    Generate past and future forecasts with clear labeling.
    Returns a combined DataFrame with 'Past Forecast' and 'Future Forecast'.
    """
    forecast_dfs = []

    for cluster_id, df in segments.items():
        if 'date' not in df.columns or 'demand' not in df.columns:
            continue

        model_name = model_map.get(cluster_id, "Prophet")

        df = df.copy()
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date']).sort_values('date')

        if df.empty:
            continue

        # Add metadata
        df['model'] = model_name
        df['cluster'] = cluster_id
        df['Segment'] = cluster_id

        # Past forecast (simple 3-month rolling average)
        df['forecast'] = df['demand'].rolling(window=3).mean().bfill()
        df['forecast_type'] = 'Past Forecast'

        # Future forecast
        last_date = df['date'].max()
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=forecast_periods,
            freq='MS'
        )

        future_df = pd.DataFrame({
            'date': future_dates,
            'forecast': df['forecast'].iloc[-1],  # flat projection
            'forecast_type': 'Future Forecast',
            'Segment': cluster_id,
            'model': model_name,
            'cluster': cluster_id,
            'demand': None  # Placeholder to align columns
        })

        forecast_dfs.append(pd.concat([df, future_df], ignore_index=True))

    combined = pd.concat(forecast_dfs, ignore_index=True)
    print(f"[✔] Generated {forecast_periods} period future forecast for {len(forecast_dfs)} segments.")
    return combined


def create_side_by_side_chart(df):
    """
    Create subplots for each segment with actual demand, past and future forecasts.
    """
    segments = df['Segment'].unique()
    num_segments = len(segments)

    fig = make_subplots(rows=num_segments, cols=1, shared_xaxes=True, subplot_titles=segments)

    for i, segment in enumerate(segments, start=1):
        seg_df = df[df['Segment'] == segment]

        # Actual Demand
        if 'demand' in seg_df.columns:
            fig.add_trace(go.Scatter(
                x=seg_df['date'],
                y=seg_df['demand'],
                mode='lines+markers',
                name=f'{segment} - Actual',
                line=dict(color='#1f77b4', width=3),
                showlegend=(i == 1)
            ), row=i, col=1)

        # Past Forecast
        past = seg_df[seg_df['forecast_type'] == 'Past Forecast']
        fig.add_trace(go.Scatter(
            x=past['date'],
            y=past['forecast'],
            mode='lines+markers',
            name=f'{segment} - Past Forecast',
            line=dict(color='#ff7f0e', dash='dash', width=2),
            showlegend=(i == 1)
        ), row=i, col=1)

        # Future Forecast
        future = seg_df[seg_df['forecast_type'] == 'Future Forecast']
        fig.add_trace(go.Scatter(
            x=future['date'],
            y=future['forecast'],
            mode='lines+markers',
            name=f'{segment} - Future Forecast',
            line=dict(color='#2ca02c', width=4),
            fill='tozeroy',
            showlegend=(i == 1)
        ), row=i, col=1)

    fig.update_layout(
        height=300 * num_segments,
        title="Demand Forecast Timeline by Segment",
        xaxis_title="Date",
        yaxis_title="Units",
        hovermode="x unified",
        template="plotly_white",
        margin=dict(t=40, b=40)
    )
    return fig
