import pandas as pd
from pathlib import Path

def finalize_forecast(df):
    """
    Save the final forecast to a CSV file.

    Args:
        df (pd.DataFrame): Final forecast DataFrame.

    Returns:
        None
    """
    print("[Step 6] Finalizing forecast...")

    output_path = Path("data/forecast_result.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"[✔] Forecast saved to {output_path}")
