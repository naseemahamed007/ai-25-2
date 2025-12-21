import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Naseem Health App",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- APPLE STYLE CSS ----------------
st.markdown("""
<style>
/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(145deg, #f8f8fa, #ffffff);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
}

/* HEADER */
.hero {
    text-align:center;
    padding:90px 20px 30px 20px;
}
.hero h1 {
    font-size:64px;
    font-weight:800;
    margin-bottom:10px;
    color:#000;
}
.hero p {
    font-size:20px;
    color:#555;
}

/* APPLE CARD DESIGN */
.card {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(20px);
    border-radius:25px;
    padding:28px;
    box-shadow:0 6px 25px rgba(0,0,0,0.08);
    margin-bottom:20px;
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow:0 12px 35px rgba(0,0,0,0.12);
}

/* SECTION HEADING */
.section {
    font-size:34px;
    font-weight:700;
    margin-bottom:25px;
    color:#111;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "started" not in st.session_state:
    st.session_state.started = False

# ---------------- LANDING PAGE ----------------
if not st.session_state.started:
    st.markdown("""
    <div class="hero">
        <h1>🍏 Naseem Health App</h1>
        <p>Your All-in-One AI Powered Health Ecosystem</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Enter Dashboard", use_container_width=True):
            st.session_state.started = True
            st.rerun()
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🍏 Naseem Health App")
menu = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Vitals", "Symptoms", "Diabetes", "Heart", "Trends", "AI (Coming Soon)", "Reports (Coming Soon)"]
)

# ----------------------------------------------------
# ---------------- DASHBOARD PAGE --------------------
# ----------------------------------------------------
if menu == "Dashboard":
    st.markdown("<div class='section'>Overall Health Summary</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class='card'>
        <h3>🧍 BMI</h3>
        <h1>24.6</h1>
        <p>Normal</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='card'>
        <h3>🩸 Blood Pressure</h3>
        <h1>118/78</h1>
        <p>Optimal</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='card'>
        <h3>❤️ Health Score</h3>
        <h1>84%</h1>
        <p>Good</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.write("Health Score Loading…")
    progress = st.progress(0)
    for i in range(101):
        progress.progress(i)
        time.sleep(0.01)
    st.success("Health Score Calculated")

# ----------------------------------------------------
# ---------------- VITALS PAGE -----------------------
# ----------------------------------------------------
elif menu == "Vitals":
    st.markdown("<div class='section'>Vitals Analyzer</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        height = col1.number_input("Height (cm)", 100, 220)
        weight = col1.number_input("Weight (kg)", 30, 200)
        sys = col2.number_input("Systolic BP", 80, 250)
        dia = col2.number_input("Diastolic BP", 40, 150)

        if st.button("Analyze Vitals"):
            bmi = round(weight / ((height/100)**2), 2)
            st.success(f"BMI: {bmi}")
            st.progress(min(int(bmi*4),100))

        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# ---------------- SYMPTOM ANALYZER ------------------
# ----------------------------------------------------
elif menu == "Symptoms":
    st.markdown("<div class='section'>AI Symptom Checker</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    symptoms = st.multiselect(
        "Select symptoms",
        ["Fever","Cough","Chest Pain","Fatigue","Frequent Urination"]
    )

    if st.button("Check"):
        if "Chest Pain" in symptoms:
            st.error("⚠️ Potential cardiac issue detected.")
        elif "Frequent Urination" in symptoms:
            st.warning("⚠️ Possible diabetes risk.")
        else:
            st.success("No major risk detected.")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# ---------------- DIABETES PAGE ---------------------
# ----------------------------------------------------
elif menu == "Diabetes":
    st.markdown("<div class='section'>Diabetes Risk</div>", unsafe_allow_html=True)

    sugar = st.number_input("Fasting Sugar (mg/dL)", 60, 300)

    if st.button("Analyze Sugar"):
        if sugar >= 126:
            st.error("High Diabetes Risk")
        elif sugar >= 100:
            st.warning("Pre-diabetic Stage")
        else:
            st.success("Normal Sugar Level")

# ----------------------------------------------------
# ---------------- HEART PAGE ------------------------
# ----------------------------------------------------
elif menu == "Heart":
    st.markdown("<div class='section'>Heart Risk Assessment</div>", unsafe_allow_html=True)

    chol = st.number_input("Cholesterol", 100, 400)
    smoke = st.selectbox("Do you smoke?", ["No","Yes"])

    if st.button("Assess Risk"):
        if chol > 240 or smoke == "Yes":
            st.error("⚠️ High Heart Risk")
        else:
            st.success("Low Heart Risk")

# ----------------------------------------------------
# ---------------- TRENDS PAGE -----------------------
# ----------------------------------------------------
elif menu == "Trends":
    st.markdown("<div class='section'>Health Trends</div>", unsafe_allow_html=True)

    df = pd.DataFrame({
        "Date": pd.date_range(end=datetime.today(), periods=10),
        "BMI":[24,24.2,24.4,24.6,24.7,24.8,25,24.9,24.8,24.7]
    })

    fig = px.line(df, x="Date", y="BMI", markers=True, title="BMI Trend Over Time")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- Coming Soon ----------------
elif menu == "AI (Coming Soon)":
    st.info("AI Symptom Intelligence, Voice Assistant & Prediction Engine Coming 🔥")

elif menu == "Reports (Coming Soon)":
    st.info("PDF Health Report Generator Coming Soon.")
