import streamlit as st

st.set_page_config(
    page_title="NasCare",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Top bar
st.markdown("<h2 style='margin-bottom:0'>NasCare — Health Companion</h2>", unsafe_allow_html=True)
st.caption("Big MVP: Dashboard • AI Assistant • Analytics • Gamification • Community")

# Navigation (simple tabs for MVP)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "AI Assistant", "Analytics", "Achievements", "Community"])

with tab1:
    st.subheader("Dashboard")
    st.write("Vitals, lifestyle logs, and status cards will appear here.")

with tab2:
    st.subheader("AI Assistant")
    st.write("Chat interface will appear here.")

with tab3:
    st.subheader("Analytics")
    st.write("Charts and insights will appear here.")

with tab4:
    st.subheader("Achievements")
    st.write("Badges and streaks will appear here.")

with tab5:
    st.subheader("Community")
    st.write("Support room and chat will appear here.")

st.sidebar.header("Quick Actions")
st.sidebar.button("Sync Data")
st.sidebar.toggle("Dark Mode", help="Toggle theme (visual only in MVP)")
