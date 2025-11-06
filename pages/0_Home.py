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

if st.sidebar.button("Logout"):
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
