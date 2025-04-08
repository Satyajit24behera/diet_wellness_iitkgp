import streamlit as st
import os
import json
import uuid

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

st.title("🩺 Personalized Diet Plan - User Input")

with st.form("user_input_form"):
    st.subheader("👤 Basic Information")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    location = st.text_input("Location")

    st.subheader("📏 Health & Lifestyle")
    height = st.number_input("Height (cm)")
    weight = st.number_input("Weight (kg)")
    activity_level = st.selectbox("Physical Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    smoking = st.checkbox("Do you smoke?")
    alcohol = st.checkbox("Do you consume alcohol?")

    st.subheader("🥦 Diet Preferences")
    diet_type = st.selectbox("Diet Type", ["No Preference", "Vegetarian", "Vegan", "Keto", "Low Carb", "High Protein"])
    allergies = st.text_input("Any known allergies? (comma-separated)")
    goal = st.selectbox("Your Health Goal", ["Weight Loss", "Muscle Gain", "Diabetes Management", "Overall Wellness"])

    st.subheader("📑 Upload Medical Report (optional)")
    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

    submitted = st.form_submit_button("Submit and Save")

if submitted:
    # Store data in session state
    user_data = {
        "name": name,
        "age": age,
        "gender": gender,
        "location": location,
        "height": height,
        "weight": weight,
        "activity_level": activity_level,
        "smoking": smoking,
        "alcohol": alcohol,
        "diet_type": diet_type,
        "allergies": allergies,
        "goal": goal,
    }

    st.session_state["user_data"] = user_data

    # Save uploaded medical file if available
    medical_file_path = None
    if uploaded_file is not None:
        medical_file_path = os.path.join("data", uploaded_file.name)
        with open(medical_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state["medical_file"] = medical_file_path

    # Generate unique user ID and save form data as JSON
    user_id = str(uuid.uuid4())
    st.session_state["user_id"] = user_id

    json_path = os.path.join("data", f"user_{user_id}.json")
    with open(json_path, "w") as f:
        json.dump(user_data, f, indent=4)

    st.success(f"✅ Data saved successfully!\n\n➡️ Proceed to the next step: Health Analysis (Page 2)")
    st.write("Saved JSON:", json_path)
    if medical_file_path:
        st.write("Uploaded Medical File:", medical_file_path)
