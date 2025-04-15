import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
API_URL = os.getenv("HF_API_URL")

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}

st.set_page_config(page_title="EduChat - HuggingFace", layout="centered")
st.title("📘 EduChat - Chapter Simplifier (Hugging Face)")
st.markdown("Explain chapters in simple terms for 9th and 10th standard teachers.")

grade = st.sidebar.selectbox("Select Grade", ["9th", "10th"])
subject = st.sidebar.selectbox("Select Subject", ["Science", "Math", "Social Science", "English", "Hindi"])

if "messages" not in st.session_state:
    st.session_state.messages = []

def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

def generate_prompt(chapter_detail):
    return f"""You are an assistant helping school teachers. Given the chapter detail, provide a simple explanation suitable for a teacher teaching grade {grade} {subject}:

Chapter Detail:
{chapter_detail}

Explanation (keep it short, clear, and suitable for students):
"""

user_input = st.text_input("Enter the chapter details...")

if st.button("Explain"):
    if user_input:
        st.session_state.messages.append(("user", user_input))
        with st.spinner("Generating explanation..."):
            prompt = generate_prompt(user_input)
            output = query_huggingface({"inputs": prompt})
        st.session_state.messages.append(("bot", output))
    else:
        st.warning("Please enter some chapter details!")

# Display chat
for sender, msg in st.session_state.messages:
    st.markdown(f"**{'🧑‍🏫 You' if sender == 'user' else '🤖 EduChat'}:** {msg}")
