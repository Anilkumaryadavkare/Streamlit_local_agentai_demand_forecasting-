import streamlit as st
import pandas as pd
from datetime import datetime

def render_scenario_stage():
    st.header("🔮 Scenario Modeling")
    
    # Scenario controls
    col1, col2 = st.columns(2)
    with col1:
        scenario_date = st.date_input("Select scenario date", datetime.now())
        impact = st.slider("Demand impact (%)", -50, 200, 10)
    with col2:
        reason = st.text_input("Scenario reason", "Promotional event")
        apply_to_cluster = st.selectbox(
            "Apply to cluster",
            options=list(st.session_state.segments.keys())  # 🛠 Fixed closing parenthesis
        )

    if st.button("💡 Apply Scenario"):
        # Apply scenario rules
        scenario_rules = {
            str(scenario_date): {
                "multiplier": 1 + (impact/100),
                "reason": reason,
                "cluster": apply_to_cluster
            }
        }
        
        # Store scenario-adjusted forecast
        original_forecast = st.session_state.forecast_df
        st.session_state.scenario_forecast = original_forecast.copy()
        
        # Apply multiplier to selected cluster and date
        cluster_mask = st.session_state.scenario_forecast['cluster'] == apply_to_cluster
        date_mask = st.session_state.scenario_forecast['date'] == pd.to_datetime(scenario_date)
        st.session_state.scenario_forecast.loc[cluster_mask & date_mask, 'forecast'] *= (1 + impact/100)
        
        st.session_state.current_stage += 1
        st.rerun()
