import sys
import os

# 🔧 Add project root to sys.path if not already present
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd

from core.data_prep import prepare_data
from core.segmentation import segment_demand
from core.model_selection import suggest_best_model
from core.forecasting import generate_forecast, create_side_by_side_chart
from core.human_override import apply_overrides
from core.finalization import finalize_forecast
from core.learning import update_learning

# ✅ AGENTS
from agents.prompt_agent import generate_prompt_clarification
from agents.summary_agent import generate_summary
from agents.memory_agent import log_session

st.set_page_config(page_title="Agentic Demand Forecasting", layout="wide")
st.title("📊 Agentic AI Forecasting Tool")

uploaded_file = st.file_uploader("Upload your demand CSV", type=["csv"])

if uploaded_file:
    # Step 1: Load & Clean
    df = pd.read_csv(uploaded_file)
    df.to_csv("data/uploaded.csv", index=False)
    df = prepare_data("data/uploaded.csv")

    # 🤖 Prompt Agent
    st.subheader("🤖 Prompt Agent: Clarifying Questions")
    context = df.head(5).to_csv(index=False)
    clarification = generate_prompt_clarification(context)
    st.info(clarification)

    st.subheader("✅ Cleaned Data")
    st.write(df)

    # Step 2: Segment
    segments = segment_demand(df)

    # Step 3: Model Selection
    model_map = {cid: suggest_best_model(seg_df) for cid, seg_df in segments.items()}
    st.markdown(f"**Selected Models:** {model_map}")

    # Step 4: Forecast
    forecast_df = generate_forecast(segments, model_map)

    # Step 5: Override
    forecast_df = apply_overrides(forecast_df)

    # Step 6: Finalize & Download
    finalize_forecast(forecast_df)

    # Step 7: Learn
    update_learning(df, forecast_df)

    # 📈 Visualization
    st.subheader("📈 Forecast Visualization")
    fig = create_side_by_side_chart(forecast_df)
    st.plotly_chart(fig, use_container_width=True)

    # 📥 Download
    st.download_button("📥 Download Forecast CSV", data=forecast_df.to_csv(index=False),
                       file_name="forecast_result.csv", mime="text/csv")

    # 📝 Summary Agent
    st.subheader("📝 Forecasting Session Summary")
    summary_text = generate_summary(len(df), len(df.columns), len(segments), model_map)
    st.success(summary_text)

    # 🧠 Memory Agent
    log_session(summary_text)
