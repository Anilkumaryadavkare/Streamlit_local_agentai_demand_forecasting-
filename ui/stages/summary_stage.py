import streamlit as st
from agents.summary_agent import generate_summary
from agents.memory_agent import log_session
from sklearn.metrics import mean_absolute_error, mean_squared_error

def render_summary_stage():
    st.header("📊 Final Output & Assumptions")

    # Forecast Assumptions
    with st.expander("🔍 Model Assumptions"):
        st.markdown("""
        **Base Forecasting Assumptions:**
        - Historical trends continue for 6 months
        - No major supply chain disruptions
        - Consistent promotional calendar
        - ±15% forecast confidence interval
        """)

    # Scenario Comparison
    if hasattr(st.session_state, 'scenario_forecast') and hasattr(st.session_state, 'forecast_df'):
        with st.expander("📈 Scenario Impact Analysis", expanded=True):
            col1, col2 = st.columns(2)
            baseline_mean = st.session_state.forecast_df['forecast'].mean()
            scenario_mean = st.session_state.scenario_forecast['forecast'].mean()
            delta_pct = ((scenario_mean - baseline_mean) / baseline_mean) * 100 if baseline_mean != 0 else 0
            with col1:
                st.metric("Baseline Forecast", round(baseline_mean, 2))
            with col2:
                st.metric("Scenario Forecast", round(scenario_mean, 2), delta=f"{delta_pct:.1f}%")

    # Additional Context from User Responses
    with st.expander("🗣️ Additional Context", expanded=True):
        user_responses = st.session_state.get("user_responses", {})
        answered_questions = {q: a for q, a in user_responses.items() if a.strip()}
        if answered_questions:
            for q, ans in answered_questions.items():
                st.markdown(f"**{q}**  \n{ans}")
        else:
            st.write("No contextual inputs were provided")

    # Data Quality Report
    st.subheader("🧹 Data Quality Report")
    col1, col2 = st.columns(2)

    error_df = st.session_state.audit_logs.get_error_df()
    log_df = st.session_state.audit_logs.get_log_df()

    invalid_dates = 0
    if not error_df.empty and 'error_type' in error_df.columns:
        invalid_dates = len(error_df[error_df['error_type'] == 'Invalid date format'])

    duplicates_removed = 0
    if not log_df.empty and 'action' in log_df.columns:
        duplicates_removed = log_df[log_df['action'] == 'Dropped duplicates']['rows_affected'].sum()

    with col1:
        st.metric("Original Rows", len(st.session_state.df_raw))
        st.metric("Invalid Dates Removed", invalid_dates)

    with col2:
        st.metric("Cleaned Rows", len(st.session_state.df_clean))
        st.metric("Duplicate Rows Removed", int(duplicates_removed))

    # Forecast Performance Metrics
    st.subheader("📈 Forecast Accuracy Metrics")
    if 'forecast_df' in st.session_state and 'actuals' in st.session_state.forecast_df.columns:
        y_true = st.session_state.forecast_df['actuals']
        y_pred = st.session_state.forecast_df['forecast']
        mape = (abs((y_true - y_pred) / y_true).mean() * 100).round(2)
        rmse = mean_squared_error(y_true, y_pred, squared=False).round(2)
        bias = (y_pred - y_true).mean().round(2)

        col1, col2, col3 = st.columns(3)
        col1.metric("MAPE (%)", mape)
        col2.metric("RMSE", rmse)
        col3.metric("Bias", bias)

    # Download Forecast
    st.download_button(
        "📥 Download Full Forecast",
        st.session_state.get('scenario_forecast', st.session_state.forecast_df).to_csv(index=False),
        file_name="forecast_report.csv"
    )

    # Start new session
    if st.button("🔄 Start New Session"):
        st.session_state.clear()
        st.rerun()
