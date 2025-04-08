import streamlit as st
import json
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from utils.pdf_generator import generate_pdf, parse_recommendations  # 📌 Use actual PDF functions

# ------------------------ Environment Setup ------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ------------------------ Streamlit Setup ------------------------
st.set_page_config(page_title="Wellness Recommendations", layout="centered")
st.title("🎯 Personalized Wellness Guide")

if "user_data" not in st.session_state or "confirmed_conditions" not in st.session_state:
    st.error("⚠️ Please complete Page 1 and 2 first.")
    st.stop()

user_data = st.session_state["user_data"]
confirmed_conditions = st.session_state["confirmed_conditions"]

# ------------------------ Recommendation Engine ------------------------
def generate_recommendations(user_data: dict, confirmed_conditions: list[str]) -> str:
    conditions_md = "\n".join(f"- {cond}" for cond in confirmed_conditions)

    prompt = f"""
    You are a health assistant. Generate a personalized wellness plan with:

    ### 👤 User Summary
    Name: {user_data.get("name")}
    Age: {user_data.get("age")}
    Goal: {user_data.get("goal")}
    Health Conditions:
    {conditions_md}

    Format your response strictly like this (plain text only, one-liners):

    Note:
    - [One-liner note]

    Health Conditions:
    - [Condition 1 and action]
    - [Condition 2 and action]

    Food Plan:
    - [One-liner food recommendation 1]
    - [One-liner food recommendation 2]

    Exercise Plan:
    - [One-liner exercise recommendation 1]
    - [One-liner exercise recommendation 2]

    Supplement Plan:
    - [One-liner supplement recommendation 1]
    - [One-liner supplement recommendation 2]
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# ------------------------ Text Cleaning (Optional) ------------------------
def clean_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()

# ------------------------ Main Streamlit Flow ------------------------
if st.button("📄 Generate Plan"):
    with st.spinner("Generating personalized recommendations..."):
        recommendations = generate_recommendations(user_data, confirmed_conditions)
        st.session_state["recommendations"] = recommendations

        # Save to local JSON file (optional)
        if "user_id" in st.session_state:
            path = os.path.join("data", f"user_{st.session_state['user_id']}.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
                data["recommendations"] = recommendations
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

# ------------------------ Output Display & Download ------------------------
if "recommendations" in st.session_state:
    st.subheader("📋 Wellness Recommendation")
    st.markdown(st.session_state["recommendations"])

    # Parse LLM output
    parsed_sections = parse_recommendations(st.session_state["recommendations"])

    # Merge with user info
    complete_content = {
        "Name": user_data.get("name", "User"),
        "Age": user_data.get("age", "N/A"),
        "Goal": user_data.get("goal", "N/A"),
        **parsed_sections
    }

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download as PDF"):
            pdf_path = generate_pdf(complete_content, output_path="wellness_guide.pdf")
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, "wellness_guide.pdf", mime="application/pdf")

    with col2:
        st.info("DOCX download removed in this version.")

    st.success("✅ All set! You can now download your plan.")
