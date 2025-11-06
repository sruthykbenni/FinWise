import streamlit as st
from utils.session_manager import validate_session, get_user, clear_session

st.set_page_config(page_title="Home — FinWise", page_icon="💰", layout="wide")

token = st.session_state.get("token")
if not (token and validate_session(token)):
    st.warning("Please login first.")
    st.stop()

username = get_user(token)
st.sidebar.success(f"Welcome, {username} 👋")

# --- Sidebar Navigation ---
st.sidebar.title("🏠 Navigation")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
st.sidebar.page_link("pages/2_Chatbot.py", label="Chatbot", icon="🤖")
st.sidebar.page_link("pages/3_Profile.py", label="Profile", icon="👤")

st.sidebar.markdown("---")
st.sidebar.text_input("🔑 OpenAI API Key", type="password", key="OPENAI_API_KEY")
st.sidebar.text_input("🔑 Groq API Key", type="password", key="GROQ_API_KEY")

if st.sidebar.button("🚪 Logout"):
    clear_session()
    st.session_state.token = None
    st.session_state.username = None
    st.success("✅ Logged out successfully!")
    st.rerun()

# --- Main Content ---
st.title("💰 Welcome to FinWise!")
st.markdown(f"""
Hi **{username}**, welcome to **FinWise — your AI-powered personal financial advisor**.

Here you can:
- Upload and analyze your transaction data  
- Visualize spending patterns and insights  
- Chat with your AI assistant for personalized financial advice  
- Download reports and summaries  

Use the sidebar to explore different sections of the app.
""", unsafe_allow_html=True)

st.markdown("---")
st.info("💡 Tip: Start from the Dashboard to upload your transaction data!")
