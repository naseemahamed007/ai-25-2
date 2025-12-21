
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# ================= SAFE AI SETUP =================
# Reads API key from environment variable
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])



def ai_doctor(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a friendly medical assistant. Give safe health guidance."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Naseem Health OS",
    page_icon="🍏",
    layout="wide"
)

# ================= THEME ENGINE =================
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
border-radius: 25px;padding: 30px;box-shadow: 0 10px 40px rgba(0,0,0,0.05);margin-bottom: 25px;}
.bigtitle {font-size: 42px;font-weight: 800;color: #000;}
.subtitle {font-size:18px;color:#333;}
</style>
"""

DARK = """
<style>
body {background: radial-gradient(circle at top, #121212, #000000) !important;}
header {visibility: hidden;}
section.main > div {padding-top: 1rem;}
.block {background: rgba(20,20,20,0.55);backdrop-filter: blur(25px);
border-radius: 25px;padding: 30px;box-shadow: 0 10px 40px rgba(0,0,0,0.45);margin-bottom: 25px;}
.bigtitle {font-size: 42px;font-weight: 800;color: #fff;}
.subtitle {font-size:18px;color:#ccc;}
</style>
"""

if st.session_state.theme == "light":
    st.markdown(LIGHT, unsafe_allow_html=True)
else:
    st.markdown(DARK, unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🍏 Naseem Health OS")
    menu = st.radio("Navigate", [
        "🏠 Dashboard",
        "📊 Vitals",
        "🩺 Symptoms",
        "🧬 Diabetes",
        "❤️ Heart",
        "📈 Trends",
        "🤖 AI Doctor",
        "🎤 Voice Assistant",
        "⚙️ Settings"
    ])

# ================= DASHBOARD =================
if menu == "🏠 Dashboard":
    st.markdown("<div class='bigtitle'>Welcome to Naseem Health OS</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your personal AI-powered health ecosystem.</div><br>", unsafe_allow_html=True)

    cols = st.columns(3)
    metrics = [("BMI", "24.6", "🧍"), ("Blood Pressure", "118/78", "🩸"), ("Health Score", "84%", "❤️")]
    for col, (label, value, icon) in zip(cols, metrics):
        with col:
            st.markdown(f"<div class='block'><h3>{icon} {label}</h3><h1>{value}</h1><p style='opacity:0.7;'>Updated Now</p></div>", unsafe_allow_html=True)

    st.markdown("<br><div class='bigtitle'>Health Score Progress</div>", unsafe_allow_html=True)
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        bar.progress(i+1)

# ================= VITALS =================
elif menu == "📊 Vitals":
    st.markdown("<div class='bigtitle'>Vitals Analyzer</div>", unsafe_allow_html=True)
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    h = c1.number_input("Height (cm)", 100, 250)
    w = c1.number_input("Weight (kg)", 30, 200)
    sys = c2.number_input("Systolic BP", 80, 250)
    dia = c2.number_input("Diastolic BP", 40, 150)

    if st.button("Analyze"):
        bmi = round(w / ((h/100)**2), 2)
        st.success(f"BMI: {bmi}")
        st.progress(min(int(bmi*4), 100))
    st.markdown("</div>", unsafe_allow_html=True)

# ================= SYMPTOMS =================
elif menu == "🩺 Symptoms":
    st.markdown("<div class='bigtitle'>Symptom Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    sy = st.multiselect("Select Symptoms", ["Fever","Cough","Chest Pain","Fatigue","Frequent Urination"])
    if st.button("Analyze Symptoms"):
        if "Chest Pain" in sy:
            st.error("⚠ Possible Cardiac Risk")
        elif "Frequent Urination" in sy:
            st.warning("⚠ Possible Diabetes Indicator")
        else:
            st.success("No immediate high-risk symptoms.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= DIABETES =================
elif menu == "🧬 Diabetes":
    st.markdown("<div class='bigtitle'>Diabetes Risk Analyzer</div>", unsafe_allow_html=True)
    sugar = st.number_input("Fasting Sugar Level (mg/dL)", 60, 300)
    if st.button("Check"):
        if sugar >= 126:
            st.error("High risk of diabetes")
        elif sugar >= 100:
            st.warning("Pre-diabetic range")
        else:
            st.success("Normal sugar level")

# ================= HEART =================
elif menu == "❤️ Heart":
    st.markdown("<div class='bigtitle'>Heart Health</div>", unsafe_allow_html=True)
    c = st.number_input("Cholesterol Level", 100, 400)
    s = st.selectbox("Do you smoke?", ["No", "Yes"])
    if st.button("Assess"):
        if c > 240 or s=="Yes":
            st.error("High heart risk")
        else:
            st.success("Healthy heart condition")

# ================= TRENDS =================
elif menu == "📈 Trends":
    st.markdown("<div class='bigtitle'>Trends & Analytics</div>", unsafe_allow_html=True)
    df = pd.DataFrame({
        "Date": pd.date_range(end=datetime.today(), periods=10),
        "BMI": [24, 24.2, 24.3, 24.5, 24.6, 24.8, 25, 24.9, 24.7, 24.6]
    })
    fig = px.line(df, x="Date", y="BMI", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ================= AI DOCTOR =================
elif menu == "🤖 AI Doctor":
    st.markdown("<div class='bigtitle'>AI Health Assistant</div>", unsafe_allow_html=True)
    user_input = st.text_area("Describe your symptoms or ask anything:")
    if st.button("Ask AI"):
        with st.spinner("AI is thinking..."):
            result = ai_doctor(user_input)
            st.write(result)

# ================= VOICE ASSISTANT =================
elif menu == "🎤 Voice Assistant":
    st.markdown("<div class='bigtitle'>Voice Assistant</div>", unsafe_allow_html=True)
    st.write("Voice input/output engine will activate once TTS/STT API is connected.")

# ================= SETTINGS =================
elif menu == "⚙️ Settings":
    st.markdown("<div class='bigtitle'>Settings</div>", unsafe_allow_html=True)
    st.write("### Theme")
    st.button("Toggle Light/Dark", on_click=toggle_theme)
    st.write("### Version")
    st.write("Naseem Health OS — Billion Dollar Edition 1.0.0")
