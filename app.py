import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AURA Health",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION ----------------
if "started" not in st.session_state:
    st.session_state.started = False

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {background: linear-gradient(120deg, #e0f7fa, #ffffff);}
.hero {text-align:center; padding:80px 20px;}
.hero h1 {font-size:64px; font-weight:800;}
.hero p {font-size:22px; color:#555;}
.card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(12px);
    border-radius:20px;
    padding:25px;
    box-shadow:0 8px 30px rgba(0,0,0,0.1);
    margin-bottom:20px;
}
.section {font-size:32px; font-weight:700; margin-bottom:20px;}
</style>
""", unsafe_allow_html=True)

# ================= LANDING PAGE =================
if not st.session_state.started:
    st.video("assets/hero.mp4", start_time=0)
    st.markdown("""
    <div class="hero">
        <h1>🧬 AURA Health</h1>
        <p>AI-Inspired Global Medical Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Enter Health Dashboard", use_container_width=True):
            st.session_state.started = True
            st.rerun()
    st.stop()

# ================= SIDEBAR =================
st.sidebar.title("🩺 AURA Health")
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard","Vitals","Symptoms","Diabetes","Heart","Trends"]
)

# ================= DASHBOARD =================
if menu == "Dashboard":
    st.markdown("<div class='section'>Health Overview</div>", unsafe_allow_html=True)

    # Animated cards sequentially
    cards = [
        {"emoji":"🧍", "title":"BMI", "value":"24.6","desc":"Normal"},
        {"emoji":"🩸", "title":"Blood Pressure","value":"118 / 78","desc":"Optimal"},
        {"emoji":"❤️","title":"Health Score","value":"84%","desc":"Good"},
    ]
    for c in cards:
        st.markdown(f"<div class='card'>{c['emoji']} {c['title']}<br><h2>{c['value']}</h2>{c['desc']}</div>", unsafe_allow_html=True)
        time.sleep(0.5)

    # Animated Health Score Progress
    st.write("Calculating Health Score...")
    my_bar = st.progress(0)
    for i in range(101):
        time.sleep(0.01)
        my_bar.progress(i)
    st.success("Health Score Calculated ✅")

# ================= VITALS =================
elif menu == "Vitals":
    st.markdown("<div class='section'>Vitals Analyzer</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    height = col1.number_input("Height (cm)", 100, 220)
    weight = col1.number_input("Weight (kg)", 30, 200)
    sys = col2.number_input("Systolic BP", 80, 250)
    dia = col2.number_input("Diastolic BP", 40, 150)

    if st.button("Analyze"):
        bmi = round(weight / ((height/100)**2), 2)
        st.success(f"BMI: {bmi}")
        st.progress(min(int(bmi*4),100))  # animated bar
    st.markdown("</div>", unsafe_allow_html=True)

# ================= SYMPTOMS =================
elif menu == "Symptoms":
    st.markdown("<div class='section'>Symptom Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    symptoms = st.multiselect(
        "Select symptoms",
        ["Fever","Cough","Chest Pain","Fatigue","Frequent Urination"]
    )
    if st.button("Analyze Symptoms"):
        if "Chest Pain" in symptoms:
            st.error("High cardiac risk detected")
        elif "Frequent Urination" in symptoms:
            st.warning("Possible diabetes risk")
        else:
            st.success("No major risk found")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= DIABETES =================
elif menu == "Diabetes":
    st.markdown("<div class='section'>Diabetes Risk</div>", unsafe_allow_html=True)
    sugar = st.number_input("Fasting Sugar (mg/dL)", 60, 300)
    if st.button("Check Risk"):
        if sugar >= 126:
            st.error("High diabetes risk")
        elif sugar >= 100:
            st.warning("Pre-diabetic stage")
        else:
            st.success("Normal sugar level")

# ================= HEART =================
elif menu == "Heart":
    st.markdown("<div class='section'>Heart Risk</div>", unsafe_allow_html=True)
    chol = st.number_input("Cholesterol", 100, 400)
    smoke = st.selectbox("Smoker?", ["No","Yes"])
    if st.button("Assess"):
        if chol>240 or smoke=="Yes":
            st.error("High heart risk")
        else:
            st.success("Low heart risk")

# ================= TRENDS =================
elif menu == "Trends":
    st.markdown("<div class='section'>Health Trends</div>", unsafe_allow_html=True)
    df = pd.DataFrame({
        "Date": pd.date_range(end=datetime.today(), periods=10),
        "BMI":[24,24.2,24.4,24.6,24.7,24.8,25,24.9,24.8,24.7]
    })
    fig = px.line(df,x="Date",y="BMI",markers=True)
    st.plotly_chart(fig,use_container_width=True)
