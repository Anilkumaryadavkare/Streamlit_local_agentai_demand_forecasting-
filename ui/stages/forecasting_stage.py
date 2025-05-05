import streamlit as st
from core.forecasting import generate_forecast, create_side_by_side_chart
from core.evaluation import evaluate_forecast_models
from core.visualization import plot_residuals

def generate_forecast_summary(forecast_df):
    if 'forecast_type' not in forecast_df.columns:
        return "Forecast type information is missing."

    past_df = forecast_df[forecast_df['forecast_type'].str.lower() == "past forecast"]
    future_df = forecast_df[forecast_df['forecast_type'].str.lower() == "future forecast"]

    summary = f"""
    - 📦 **{forecast_df['sku'].nunique()} SKUs** across **{forecast_df['dc_id'].nunique()} DCs** and **{forecast_df['plant_id'].nunique()} plants**
    - 🔢 **{forecast_df['cluster'].nunique()} clusters** used for segmentation
    - 🤖 Forecasts generated using **{', '.join(map(str, forecast_df['model'].dropna().unique()))}**
    - 🕰️ Historical period covered: **{past_df['date'].min().date()} to {past_df['date'].max().date()}**
    - 📈 Forecast horizon: **{future_df['date'].min().date()} to {future_df['date'].max().date()}** (if available)
    - 📊 Past records: **{len(past_df)} rows**, Future forecasts: **{len(future_df)} rows**
    """
    return summary


def render_forecasting_stage():
    st.header("📈 Phase 4: Forecasting")

    if st.session_state.forecast_df is None:
        with st.spinner("Generating forecasts..."):
            st.session_state.forecast_df = generate_forecast(
                st.session_state.segments, 
                st.session_state.model_map
            )

    forecast_df = st.session_state.forecast_df

    # 📜 Forecast Assumptions
    st.subheader("📜 Forecast Assumptions")
    st.markdown("""
    - Economic conditions remain stable  
    - No changes in distribution partners  
    - Historical trends continue  
    - Cleaned data is outlier-free  
    """)

    # 📊 Model Performance
    st.subheader("📊 Model Performance Summary")
    if not forecast_df.empty:
        model_metrics_df = evaluate_forecast_models(forecast_df)
        st.dataframe(
            model_metrics_df.rename(columns={
                'cluster': 'Cluster',
                'model': 'Model',
                'mape': 'MAPE (%)',
                'rmse': 'RMSE'
            }), 
            use_container_width=True
        )
    else:
        st.warning("No forecast data to evaluate")

    # 🧠 Model Selection
    st.subheader("🧠 Select Preferred Model (Optional)")
    if not forecast_df.empty:
        clusters = forecast_df['cluster'].unique()
        user_model_choices = {}
        
        for cluster in clusters:
            models = model_metrics_df[model_metrics_df['cluster'] == cluster]['model'].unique()
            default = st.session_state.model_map.get(cluster, models[0] if len(models) > 0 else None)
            if default:
                selected = st.selectbox(
                    f"Model for Cluster {cluster}",
                    models,
                    index=list(models).index(default)
                )
                user_model_choices[cluster] = selected
        st.session_state.user_model_map = user_model_choices

    # 🪄 Visualization
    st.subheader("🪄 Visualization Options")
    chart_type = st.radio("Chart Type", ["Trend View"])
    
    if chart_type == "Trend View":
        fig = create_side_by_side_chart(forecast_df)
    else:
        fig = plot_residuals(forecast_df)
    
    st.plotly_chart(fig, use_container_width=True)

    # 🔍 Forecast Summary
    st.subheader("🧾 Forecast Summary")
    summary = generate_forecast_summary(forecast_df)
    st.markdown(summary)

    # 📦 Download Forecasts
    st.subheader("📦 Forecast Data Output")
    if not forecast_df.empty:
        st.download_button(
            "📥 Download Forecasts (CSV)",
            forecast_df.to_csv(index=False),
            file_name="forecasts.csv"
        )
    
    if st.button("✅ Approve Forecasts & Continue"):
        st.session_state.current_stage += 1
        st.rerun()
