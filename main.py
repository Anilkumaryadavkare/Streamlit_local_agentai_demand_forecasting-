from core.data_prep import prepare_data
from core.segmentation import segment_demand
from core.model_selection import suggest_best_model
from core.forecasting import generate_forecast
from core.human_override import apply_overrides
from core.finalization import finalize_forecast
from core.learning import update_learning


def run_pipeline(filepath):
    print("[Step 1] Loading and cleaning data...")
    df = prepare_data(filepath)

    print("[Step 2] Segmenting SKUs using KMeans...")
    segments = segment_demand(df)

    print("[Step 3] Selecting best models per cluster...")
    model_map = {}
    for cluster_id, group_df in segments.items():
        best_model = suggest_best_model(group_df)
        model_map[cluster_id] = best_model
    print(f"[✔] Model suggestion done: {model_map}")

    print("[Step 4] Generating forecasts...")
    forecast_df = generate_forecast(segments, model_map)

    print("[Step 5] Awaiting planner overrides... (none applied for now)")
    forecast_df = apply_overrides(forecast_df)

    print("[Step 6] Finalizing forecast...")
    finalize_forecast(forecast_df)

    print("[Step 7] Logging learning...")
    update_learning(df, forecast_df)

    print("✅ Forecasting pipeline completed.")


if __name__ == "__main__":
    run_pipeline("data/sample.csv")
