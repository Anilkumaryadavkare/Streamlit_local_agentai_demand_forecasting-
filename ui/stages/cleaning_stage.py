import streamlit as st
from core.data_cleaning import clean_data

def render_cleaning_stage():
    st.header("🧹 Phase 1: Data Cleaning")
    
    if st.session_state.df_clean is None:
        with st.spinner("Cleaning data..."):
            df_clean, audit = clean_data(st.session_state.df_raw)
            st.session_state.df_clean = df_clean
            st.session_state.audit_logs = audit

    st.subheader("Cleaned Data Preview")
    st.dataframe(st.session_state.df_clean.head())

    with st.expander("🔍 Cleaning Audit Details"):
        # st.write(f"Rows removed: {len(st.session_state.df_raw) - len(st.session_state.df_clean)}")
        st.download_button("Download Action Log", 
                         st.session_state.audit_logs.get_log_df().to_csv(index=False), 
                         file_name="action_log.csv")
        
        if st.checkbox("Show raw audit log"):
            st.dataframe(st.session_state.audit_logs.get_log_df())

    if st.button("✅ Approve Cleaning & Continue", key="approve_clean"):
        st.session_state.current_stage += 1
        st.rerun()