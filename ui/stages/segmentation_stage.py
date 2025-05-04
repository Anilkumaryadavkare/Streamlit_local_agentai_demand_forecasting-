import streamlit as st
from core.segmentation import segment_demand

def render_segmentation_stage():
    st.header("🗂️ Phase 2: Demand Segmentation")
    
    if st.session_state.segments is None:
        with st.spinner("Clustering SKUs..."):
            st.session_state.segments = segment_demand(st.session_state.df_clean)

    st.subheader(f"Segments Created: {len(st.session_state.segments)}")
    
    selected_cluster = st.selectbox("View Cluster", options=list(st.session_state.segments.keys()))
    st.dataframe(st.session_state.segments[selected_cluster])

    if st.button("✅ Approve Segmentation & Continue", key="approve_segments"):
        st.session_state.current_stage += 1
        st.rerun()