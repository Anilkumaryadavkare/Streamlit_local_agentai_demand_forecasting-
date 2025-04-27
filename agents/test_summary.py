from summary_agent import generate_summary

if __name__ == "__main__":
    context = """
    - Cleaned 9 rows and 5 columns.
    - Segmented SKUs into 4 clusters.
    - Selected ARIMA and Prophet models for forecasting.
    - Generated forecasts using rolling average.
    - No manual overrides applied.
    - Finalized forecast and saved results.
    """
    
    summary = generate_summary(context)
    print("📝 Forecasting Session Summary:")
    print(summary)
