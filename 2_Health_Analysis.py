import streamlit as st
import json
import os
from utils.condition_matcher import match_conditions

st.title("🧠 Health Analysis & Condition Matching")

# Check user data from Page 1
if "user_data" not in st.session_state:
    st.error("⚠️ Please complete Page 1 first.")
    st.stop()

user_data = st.session_state["user_data"]

# Optional medical report
medical_report = st.text_area("📄 Paste any medical report or notes (optional)")

# Trigger condition matching using Gemini
if st.button("🔍 Analyze & Suggest Conditions"):
    with st.spinner("Analyzing..."):
        suggestions = match_conditions(user_data, medical_report)
        st.session_state["condition_suggestions"] = suggestions

# Display results
if "condition_suggestions" in st.session_state:
    st.subheader("🧩 Suggested Conditions")
    st.markdown(st.session_state["condition_suggestions"])

    # Let user select relevant ones
    st.markdown("✅ **Select relevant health conditions**")
    selected = st.multiselect(
        "Choose the conditions that apply:",
        options=[line.strip("- ").strip() for line in st.session_state["condition_suggestions"].split("\n") if line.startswith("-")]
    )

    if selected:
        st.session_state["confirmed_conditions"] = selected
        st.success("Conditions confirmed! You can continue to the next step.")
