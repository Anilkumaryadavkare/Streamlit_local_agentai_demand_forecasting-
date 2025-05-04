import streamlit as st
from agents.prompt_agent import generate_clarifying_questions

def render_prompt_agent_stage():
    st.header("❓ Contextual Clarifications (Optional)")
    
    # Generate 4-5 questions max
    if not st.session_state.user_responses:
        context = st.session_state.df_clean.head(5).to_csv(index=False)
        questions = generate_clarifying_questions(context)[:4]  # Max 4 questions
        st.session_state.questions = questions
        st.session_state.user_responses = {q: "" for q in questions}

    # Display with "optional" labels
    st.markdown("Help improve accuracy (optional):")
    for idx, question in enumerate(st.session_state.questions):
        response = st.text_input(
            f"Q{idx+1}: {question} (optional)",
            value=st.session_state.user_responses[question],
            key=f"q_{idx}"
        )
        st.session_state.user_responses[question] = response

    # Always allow proceeding
    if st.button("➡️ Continue to Segmentation"):
        st.session_state.current_stage += 1
        st.rerun()