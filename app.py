import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ================= SAFE AI SETUP =================
model_name = "distilgpt2"  # small and fast
token = st.secrets["huggingface"]["api_key"]

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
    return tokenizer, model

tokenizer, model = load_model()

def ai_doctor(prompt):
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=100)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Naseem Health OS", page_icon="🍏", layout="wide")

# ================= THEME =================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

LIGHT = """
<style>
body {background: #f5f7fa !important;}
header {visibility: hidden;}
section.main > div {padding-top: 1rem;}
.block {background: rgba(255,255,255,0.65);backdrop-filter: blur(25px);
border-radius: 25px;padding: 20px;box-shadow: 0 10px 30px rgba(0,0,0,0.05);margin-bottom: 20px;}
.bigtitle {font-size: 36px;font-weight: 800;color: #000;}
.subtitle {font-size:16px;color:#333;}
</style>
"""

DARK = """
<style>
body {background: #121212 !important;}
header {visibility: hidden;}
section.main > div {padding-top: 1rem;}
.block {background: rgba(30,30,30,0.55);backdrop-filter: blur(15px);
border-radius: 20px;padding: 20px;box-shadow: 0 10px 30px rgba(0,0,0,0.45);margin-bottom: 20px;}
.bigtitle {font-size: 36px;font-weight: 800;color: #fff;}
.subtitle {font-size:16px;color:#ccc;}
</style>
"""

st.markdown(LIGHT if st.session_state.theme=="light" else DARK, unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🍏 Naseem Health OS")
    menu = st.radio("Navigate", [
        "🏠 Dashboard","📊 Vitals","🩺 Symptoms","🧬 Diabetes","❤️ Heart",
        "📈 Trends","🤖 AI Doctor","⚙️ Settings"
    ])

# ================= DASHBOARD =================
if menu=="🏠 Dashboard":
    st.markdown("<div class='bigtitle'>Welcome to Naseem Health OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your personal AI-powered health ecosystem.</div><br>", unsafe_allow_html=True)

    cols = st.columns(3)
    metrics = [("BMI","24.6","🧍"),("BP","118/78","🩸"),("Health Score","84%","❤️")]
    for col, (label,value,icon) in zip(cols, metrics):
        with col:
            st.markdown(f"<div class='block'><h3>{icon} {label}</h3><h1>{value}</h1></div>", unsafe_allow_html=True)

# ================= AI DOCTOR =================
elif menu=="🤖 AI Doctor":
    st.markdown("<div class='bigtitle'>AI Health Assistant</div>", unsafe_allow_html=True)
    user_input = st.text_area("Describe your symptoms or ask anything:")
    if st.button("Ask AI"):
        with st.spinner("AI is thinking..."):
            result = ai_doctor(user_input)
            st.write(result)

# ================= SETTINGS =================
elif menu=="⚙️ Settings":
    st.markdown("<div class='bigtitle'>Settings</div>", unsafe_allow_html=True)
    st.button("Toggle Light/Dark", on_click=toggle_theme)
    st.write("Version 1.0 - Light & Fast Edition")
