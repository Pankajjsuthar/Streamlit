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

st.set_page_config(page_title="EduChat - Essay Title Generator", layout="centered")
st.title("✍️ EduChat - Essay Title Generator (Hugging Face)")
st.markdown("Provide the essay content, and get a suitable title suggestion for it.")

if "messages" not in st.session_state:
    st.session_state.messages = []

def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

def generate_prompt(essay_content):
    return f"""You are an assistant helping people generate suitable titles for essays. Given the essay content, provide a creative and concise title that represents the main theme of the essay:

Essay Content:
{essay_content}

Suggested Title:
"""

user_input = st.text_area("Enter the essay content...")

if st.button("Generate Title"):
    if user_input:
        st.session_state.messages.append(("user", user_input))
        with st.spinner("Generating title..."):
            prompt = generate_prompt(user_input)
            output = query_huggingface({"inputs": prompt})
        st.session_state.messages.append(("bot", output))
    else:
        st.warning("Please enter some essay content!")

# Display chat
for sender, msg in st.session_state.messages:
    st.markdown(f"**{'📝 You' if sender == 'user' else '🤖 EduChat'}:** {msg}")
