import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import os
from dotenv import load_dotenv

# -----------------------------
# Setup
# -----------------------------
load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.set_page_config(
    page_title="NasCare",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h2 style='margin-bottom:0'>NasCare — Health Companion</h2>", unsafe_allow_html=True)
st.caption("Big MVP: Dashboard • AI Assistant • Analytics • Gamification • Community")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "AI Assistant", "Analytics", "Achievements", "Community"])

# -----------------------------
# Dashboard (Vitals + Lifestyle)
# -----------------------------
with tab1:
    st.subheader("Health Dashboard")

    # Fetch vitals from Supabase
    vitals = supabase.table("health_metrics").select("*").execute()
    if vitals.data:
        df_vitals = pd.DataFrame(vitals.data)
        for metric in df_vitals["metric_type"].unique():
            latest = df_vitals[df_vitals["metric_type"] == metric].sort_values("timestamp").iloc[-1]
            color = {"Green": "✅", "Yellow": "⚠️", "Red": "❌"}.get(latest["status"], "ℹ️")
            st.metric(label=f"{metric} {color}", value=latest["value"], delta=None)
    else:
        st.info("No vitals logged yet.")

    st.subheader("Lifestyle Logs")
    lifestyle = supabase.table("lifestyle_logs").select("*").execute()
    if lifestyle.data:
        df_life = pd.DataFrame(lifestyle.data)
        latest = df_life.sort_values("timestamp").iloc[-1]
        st.write(f"💤 Sleep: {latest['sleep_hours']} hrs")
        st.write(f"💧 Hydration: {latest['hydration_ml']} ml")
        st.write(f"🏃 Exercise: {latest['exercise_minutes']} mins")
        st.write(f"🥗 Diet Score: {latest['diet_score']}")
        st.write(f"🙂 Mood Score: {latest['mood_score']}")
    else:
        st.info("No lifestyle logs yet.")

# -----------------------------
# AI Assistant
# -----------------------------
with tab2:
    st.subheader("AI Health Assistant")

    user_message = st.text_input("Type your health question:")
    if st.button("Ask AI"):
        if user_message:
            # Save to Supabase
            supabase.table("chat_history").insert({"message": user_message, "ai_response": "AI response placeholder"}).execute()
            st.chat_message("user").write(user_message)
            st.chat_message("assistant").write("This is where AI would interpret your metrics and give lifestyle tips.")
        else:
            st.warning("Please enter a message.")

    # Show past chat
    history = supabase.table("chat_history").select("*").execute()
    if history.data:
        for chat in history.data[-5:]:
            st.chat_message("user").write(chat["message"])
            st.chat_message("assistant").write(chat["ai_response"])

# -----------------------------
# Analytics
# -----------------------------
with tab3:
    st.subheader("Analytics & Insights")

    vitals = supabase.table("health_metrics").select("*").execute()
    if vitals.data:
        df_vitals = pd.DataFrame(vitals.data)
        fig = px.line(df_vitals, x="timestamp", y="value", color="metric_type", title="Vitals Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No analytics data yet.")

# -----------------------------
# Achievements
# -----------------------------
with tab4:
    st.subheader("Achievements & Gamification")

    achievements = supabase.table("achievements").select("*").execute()
    if achievements.data:
        df_badges = pd.DataFrame(achievements.data)
        for _, row in df_badges.iterrows():
            st.success(f"🏅 {row['badge_name']} — Streak: {row['streak_count']} days")
    else:
        st.info("No achievements yet.")

# -----------------------------
# Community
# -----------------------------
with tab5:
    st.subheader("Community Room")

    room = "Diabetes"
    message = st.text_input("Write a message to the community:")
    if st.button("Send"):
        if message:
            supabase.table("community_messages").insert({"room": room, "message": message}).execute()
            st.success("Message sent!")
        else:
            st.warning("Please enter a message.")

    messages = supabase.table("community_messages").select("*").eq("room", room).execute()
    if messages.data:
        for msg in messages.data[-10:]:
            st.write(f"👤 {msg['user_id']}: {msg['message']} ({msg['timestamp']})")
    else:
        st.info("No messages yet.")
