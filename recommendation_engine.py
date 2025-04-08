import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_recommendations(user_data: dict, confirmed_conditions: list[str]) -> str:
    conditions_md = "\n".join(f"- {cond}" for cond in confirmed_conditions)

    prompt = f"""
    You are a health assistant. Generate a personalized wellness plan with:

    ### 👤 User Summary
    Name: {user_data.get("name")}
    Age: {user_data.get("age")}
    Goal: {user_data.get("goal")}

    ### 🧠 Confirmed Health Conditions
    {conditions_md}

    ### 🍽️ Food Plan
    - Foods to eat (with reasoning)
    - Foods to avoid

    ### 🏃 Exercise Plan
    - Weekly plan based on goal & conditions

    ### 💊 Supplement Suggestions
    - If any deficiencies apply
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
