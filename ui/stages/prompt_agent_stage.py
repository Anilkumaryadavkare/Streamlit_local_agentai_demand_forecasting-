# prompt_agent_stage.py
import streamlit as st

STATIC_QUESTIONS = [
    {
        "key": "promotions",
        "text": "Will there be any planned promotions or discounts during the forecast period?",
        "input_type": "text",
        "examples": "Examples: '20%', 'Flat ₹100 off'",
        "default": ""
    },
    {
        "key": "seasonal_events",
        "text": "Should seasonal events be considered this period?",
        "input_type": "yesno_dropdown",
        "options": ["Diwali", "Eid", "Back to School", "Year-End", "Custom Event"],
        "default": "No"
    },
    {
        "key": "supply_changes",
        "text": "Are any significant supply or product availability changes expected?",
        "input_type": "dropdown",
        "options": ["No Change", "Shortage Expected", "Excess Inventory", "Product Exit"],
        "default": "No Change"
    },
    {
        "key": "economic_conditions",
        "text": "Are broader economic conditions expected to influence demand?",
        "input_type": "dropdown",
        "options": ["Inflation", "Recession", "Currency Volatility", "Policy Shift", "None"],
        "default": "None"
    },
    {
        "key": "competitor_actions",
        "text": "Do you anticipate competitor actions affecting demand?",
        "input_type": "dropdown",
        "options": ["Yes", "No", "Not Sure"],
        "default": "No"
    },
    {
        "key": "price_changes",
        "text": "Have there been any recent price changes for this product/category?",
        "input_type": "yesno_text",
        "examples": "Examples: 'Yes - Price up by 10%', 'No'",
        "default": "No"
    }
]

def render_prompt_agent_stage():
    st.header("❓ Contextual Clarifications (Optional)")
    
    # Initialize responses with defaults
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = {}
    for question in STATIC_QUESTIONS:
        key = question["key"]
        if key not in st.session_state.user_responses:
            st.session_state.user_responses[key] = question.get("default", "")

    st.markdown("Help improve accuracy (optional):")
    
    for idx, question in enumerate(STATIC_QUESTIONS):
        st.markdown(f"**Q{idx+1}: {question['text']}**")
        response = None
        
        # Text input with placeholder
        if question["input_type"] == "text":
            response = st.text_input(
                label=" ",
                value=st.session_state.user_responses[question["key"]],
                placeholder=question["examples"],
                key=f"text_{question['key']}"
            )
            
        # Yes/No with dropdown
        elif question["input_type"] == "yesno_dropdown":
            current_value = st.session_state.user_responses[question["key"]]
            init_yes = current_value.startswith("Yes:") if current_value else False
            
            col1, col2 = st.columns([2, 4])
            with col1:
                yesno = st.radio(
                    label="Select:",
                    options=["Yes", "No"],
                    index=0 if init_yes else 1,
                    key=f"radio_{question['key']}"
                )
            with col2:
                if yesno == "Yes":
                    event = st.selectbox(
                        label="Choose event:",
                        options=question["options"],
                        index=question["options"].index(current_value.split(": ")[1]) 
                        if init_yes else 0,
                        key=f"dropdown_{question['key']}"
                    )
                    response = f"Yes: {event}"
                else:
                    response = "No"
                    
        # Simple dropdown
        elif question["input_type"] == "dropdown":
            current_value = st.session_state.user_responses[question["key"]]
            index = question["options"].index(current_value) if current_value in question["options"] else 0
            response = st.selectbox(
                label=" ",
                options=question["options"],
                index=index,
                key=f"dropdown_{question['key']}"
            )
            
        # Yes/No with text input
        elif question["input_type"] == "yesno_text":
            current_value = st.session_state.user_responses[question["key"]]
            init_yes = current_value.startswith("Yes -") if current_value else False
            
            col1, col2 = st.columns([2, 4])
            with col1:
                yesno = st.radio(
                    label=" ",
                    options=["Yes", "No"],
                    index=0 if init_yes else 1,
                    key=f"radio_{question['key']}"
                )
            with col2:
                if yesno == "Yes":
                    details = st.text_input(
                        label="Details:",
                        value=current_value.split(" - ")[1] if init_yes else "",
                        placeholder=question["examples"],
                        key=f"text_{question['key']}"
                    )
                    response = f"Yes - {details}" if details else "Yes - "
                else:
                    response = "No"
        
        # Update session state
        if response:
            st.session_state.user_responses[question["key"]] = response
        
        st.markdown("---")

    if st.button("➡️ Continue to Segmentation"):
        st.session_state.current_stage += 1
        st.rerun()