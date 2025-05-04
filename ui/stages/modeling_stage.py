import streamlit as st
from core.model_selection import suggest_best_model

def render_modeling_stage():
    st.header("🤖 Phase 3: Model Selection")
    
    if st.session_state.model_map is None:
        with st.spinner("Selecting best models..."):
            st.session_state.model_map = {
                cid: suggest_best_model(seg_df) 
                for cid, seg_df in st.session_state.segments.items()
            }

    st.subheader("Selected Models by Cluster")
    st.write(st.session_state.model_map)

    if st.button("✅ Approve Models & Continue", key="approve_models"):
        st.session_state.current_stage += 1
        st.rerun()