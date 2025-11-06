import streamlit as st
from utils.session_manager import validate_session, get_user

st.set_page_config(page_title="FinWise Home", page_icon="💰", layout="wide")

# Validate session
token = st.session_state.get("token")
if not (token and validate_session(token)):
    st.warning("Please login first.")
    st.stop()

username = get_user(token)
st.sidebar.success(f"Welcome, {username} 👋")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="Home", icon="")
st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
st.sidebar.page_link("pages/2_Chatbot.py", label="Chatbot", icon="🤖")
st.sidebar.page_link("pages/3_Profile.py", label="Profile", icon="👤")

st.sidebar.markdown("---")
st.sidebar.text_input("🔑 OpenAI API Key", type="password", key="OPENAI_API_KEY")
st.sidebar.text_input("🔑 Groq API Key", type="password", key="GROQ_API_KEY")


st.title("💰 Welcome to FinWise!")
st.markdown(f"""
Hi **{username}**, welcome to **FinWise — your AI-powered personal financial advisor**.  
Here you can:
- Upload and analyze your transaction data.
- Visualize spending trends and insights.
- Chat with your AI assistant for personalized advice.
- View and download monthly reports.

Use the sidebar to navigate between sections.
""", unsafe_allow_html=True)

# Option to logout
if st.sidebar.button("Logout"):
    from utils.session_manager import clear_session
    clear_session()
    st.session_state.token = None
    st.session_state.username = None
    st.success("✅ Logged out successfully!")
    st.rerun()

st.markdown("---")
st.markdown("💡 *Tip:* Head to the Dashboard to start exploring your financial data!*")
