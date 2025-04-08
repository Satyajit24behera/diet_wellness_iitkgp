import streamlit as st
from PIL import Image

# Set up page config
st.set_page_config(page_title="Welcome", layout="centered")

# Centered logo and title section
st.markdown("<style>h1, h2, h3 {text-align: center;} .center {text-align: center;}</style>", unsafe_allow_html=True)

# Load and display the logo
image = Image.open("assets/iitkgp_header.png")  # 📌 Make sure image.png is in the same directory or provide full path
st.image(image, width=1500)

# Title and author info
st.markdown("##  **Personalized Wellness Guide**", unsafe_allow_html=True)
st.markdown("### By **Satyajit Behera**", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>IIT KHARAGPUR</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>BTP-2</div>", unsafe_allow_html=True)
st.markdown("---")

# Welcome message
st.markdown("### 👋 Welcome to your AI-Diet and wellness assistant!")
st.markdown("Use the **sidebar** to navigate through the steps and generate your personalized plan based on your health and wellness goals.")

# Optional: Call to action or tips
st.info("Start by entering your basic details under **User Input**.")
