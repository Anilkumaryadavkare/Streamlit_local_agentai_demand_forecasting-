import pandas as pd

def apply_scenario(forecast_df, scenario_rules):
    """
    Adjust forecasts based on user-defined scenarios.
    Example rules: {"2024-06": {"multiplier": 1.2, "reason": "Summer promo"}}
    """
    adjusted = forecast_df.copy()
    for date, params in scenario_rules.items():
        mask = adjusted['date'] == pd.to_datetime(date)
        adjusted.loc[mask, 'forecast'] *= params['multiplier']
        adjusted.loc[mask, 'scenario_note'] = params['reason']
    return adjusted