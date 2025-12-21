import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Naseem Medical Assistant",
    page_icon="🩺",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main {background-color:#f6f8fb;}
.card {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);
}
.big {font-size:34px;font-weight:700;}
.sub {color:#6c757d;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False

# ---------------- LOGIN ----------------
if not st.session_state.logged:
    st.markdown("<div class='big'>🩺 Global Medical Assistant</div>", unsafe_allow_html=True)
    st.write("Login to continue")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user != "" and pwd != "":
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Enter credentials")
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏥 Navigation")
menu = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Patient Profile",
        "Vitals Analyzer",
        "Symptom Checker",
        "Diabetes Risk",
        "Heart Risk",
        "Medication Tracker",
        "Health Trends",
        "Download Report"
    ]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.markdown("<div class='big'>Health Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>World-class digital health overview</p>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Health Score", "84%", "+5%")
    c2.metric("BMI", "24.7", "Normal")
    c3.metric("BP", "118/78", "Optimal")
    c4.metric("Risk Level", "Low")

    st.success("✅ You are currently in a healthy range. Maintain lifestyle.")

# ---------------- PROFILE ----------------
elif menu == "Patient Profile":
    st.title("👤 Patient Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    st.success("Profile Saved")

# ---------------- VITALS ----------------
elif menu == "Vitals Analyzer":
    st.title("🧪 Vitals Analyzer")

    col1, col2 = st.columns(2)
    height = col1.number_input("Height (cm)", 100, 220)
    weight = col1.number_input("Weight (kg)", 30, 200)
    sys = col2.number_input("BP Systolic", 80, 250)
    dia = col2.number_input("BP Diastolic", 40, 150)

    if st.button("Analyze"):
        bmi = round(weight / ((height/100)**2), 2)
        st.info(f"BMI: {bmi}")

        if bmi < 18.5:
            st.warning("Underweight – nutritional improvement needed")
        elif bmi < 25:
            st.success("Normal – excellent")
        elif bmi < 30:
            st.warning("Overweight – exercise recommended")
        else:
            st.error("Obese – medical guidance required")

        if sys >= 140 or dia >= 90:
            st.error("High BP detected – consult doctor")
        else:
            st.success("Blood pressure normal")

# ---------------- SYMPTOMS ----------------
elif menu == "Symptom Checker":
    st.title("🧠 Smart Symptom Checker")

    symptoms = st.multiselect(
        "Select Symptoms",
        [
            "Fever", "Cough", "Headache", "Chest Pain",
            "Shortness of Breath", "Fatigue",
            "Frequent Urination", "Excessive Thirst"
        ]
    )

    if st.button("Analyze Symptoms"):
        if "Chest Pain" in symptoms or "Shortness of Breath" in symptoms:
            st.error("🚨 Possible heart or lung emergency")
            st.write("AI Advice: Seek immediate medical attention.")
        elif "Frequent Urination" in symptoms and "Excessive Thirst" in symptoms:
            st.warning("⚠️ Possible diabetes")
            st.write("AI Advice: Get blood sugar tested.")
        elif "Fever" in symptoms:
            st.info("Possible infection")
            st.write("AI Advice: Rest and hydration recommended.")
        else:
            st.success("No serious condition detected")

# ---------------- DIABETES ----------------
elif menu == "Diabetes Risk":
    st.title("🩸 Diabetes Risk")
    sugar = st.number_input("Fasting Sugar (mg/dL)", 60, 300)
    if st.button("Check Risk"):
        if sugar >= 126:
            st.error("High diabetes risk")
        elif sugar >= 100:
            st.warning("Pre-diabetic stage")
        else:
            st.success("Normal sugar level")

# ---------------- HEART ----------------
elif menu == "Heart Risk":
    st.title("❤️ Heart Risk")
    chol = st.number_input("Cholesterol", 100, 400)
    smoke = st.selectbox("Smoker?", ["No", "Yes"])

    if st.button("Assess"):
        if chol > 240 or smoke == "Yes":
            st.error("High heart disease risk")
        else:
            st.success("Low heart risk")

# ---------------- MEDICATION ----------------
elif menu == "Medication Tracker":
    st.title("💊 Medication Tracker")
    med = st.text_input("Medicine Name")
    time = st.time_input("Time")
    days = st.number_input("Duration (days)", 1, 365)
    if st.button("Save"):
        st.success("Medication schedule saved")

# ---------------- TRENDS ----------------
elif menu == "Health Trends":
    st.title("📈 Health Trends")
    df = pd.DataFrame({
        "Date": pd.date_range(end=datetime.today(), periods=10),
        "BMI": [24,24.2,24.4,24.6,24.7,24.8,25,24.9,24.8,24.7]
    })
    fig = px.line(df, x="Date", y="BMI", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- PDF REPORT ----------------
elif menu == "Download Report":
    st.title("📄 Download Health Report")

    if st.button("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Global Medical Assistant – Health Report", ln=True)
        pdf.cell(0, 10, "Status: Normal", ln=True)
        pdf.output("health_report.pdf")
        st.success("Report generated as health_report.pdf")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚠️ Educational & screening use only. Not a replacement for doctors.")
