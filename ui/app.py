# app.py
import sys
import os
import streamlit as st
import pandas as pd

# Project root setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from stages.cleaning_stage import render_cleaning_stage
from stages.prompt_agent_stage import render_prompt_agent_stage
from stages.segmentation_stage import render_segmentation_stage
from stages.modeling_stage import render_modeling_stage
from stages.forecasting_stage import render_forecasting_stage
from stages.scenario_stage import render_scenario_stage
from stages.summary_stage import render_summary_stage

# Session state initialization
if 'current_stage' not in st.session_state:
    st.session_state.update({
        'current_stage': 0,
        'df_raw': None,
        'df_clean': None,
        'audit_logs': None,
        'user_responses': {},
        'segments': None,
        'model_map': None,
        'forecast_df': None,
        'scenario_forecast': None
    })

st.set_page_config(page_title="Agentic Forecasting", layout="wide")
st.title("📊 Demand Forecasting Workflow")

STAGES = ["Upload", "Cleaning", "Clarifications", "Segmentation", 
         "Modeling", "Forecasting", "Scenario Modeling", "Summary"]
progress = st.session_state.current_stage / (len(STAGES)-1)
st.progress(progress, text=f"Current Stage: {STAGES[st.session_state.current_stage]}")

# File upload
uploaded_file = st.file_uploader("Upload CSV", type=["csv"], key="file_uploader")

# Stage routing
if uploaded_file:
    if st.session_state.current_stage == 0:
        st.session_state.df_raw = pd.read_csv(uploaded_file)
        st.session_state.current_stage += 1

    if st.session_state.current_stage >= 1:
        render_cleaning_stage()

    if st.session_state.current_stage >= 2:
        render_prompt_agent_stage()

    if st.session_state.current_stage >= 3:
        render_segmentation_stage()

    if st.session_state.current_stage >= 4:
        render_modeling_stage()

    if st.session_state.current_stage >= 5:
        render_forecasting_stage()

    if st.session_state.current_stage >= 6:
        render_scenario_stage()

    if st.session_state.current_stage >= 7:
        render_summary_stage()

# Navigation controls
if st.session_state.current_stage > 0:
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◀ Previous Stage"):
            st.session_state.current_stage = max(0, st.session_state.current_stage - 1)
            st.rerun()