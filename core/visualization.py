import plotly.express as px

def plot_residuals(forecast_df):
    df = forecast_df.copy()
    df["Residual"] = df["Forecast"] - df["Actual"]
    
    fig = px.line(df, x="Date", y="Residual", color="Segment",
                  title="Residuals Over Time (Forecast - Actual)")
    fig.update_layout(xaxis_title="Date", yaxis_title="Residual")
    return fig
