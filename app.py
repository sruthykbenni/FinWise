# app.py
import streamlit as st
from utils.auth import init_db, verify_user, create_user
from utils.session_manager import create_session, validate_session, clear_session
import os

st.set_page_config(page_title="FinWise", page_icon="💰", layout="wide")

init_db()

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

# --- LOGIN / SIGNUP UI ---
def login_ui():
    st.markdown("<h2 style='text-align:center;'>💰 FinWise — Login</h2>", unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        if login_btn:
            if verify_user(user, pwd):
                token = create_session(user)
                st.session_state.username = user
                st.session_state.token = token
                st.session_state.active_page = "Home"
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def signup_ui():
    st.markdown("<h2 style='text-align:center;'>🆕 Create Account</h2>", unsafe_allow_html=True)
    with st.form("signup_form"):
        u = st.text_input("Choose Username")
        p = st.text_input("Choose Password", type="password")
        s_btn = st.form_submit_button("Sign up")
        if s_btn:
            try:
                create_user(u, p)
                st.success("Account created. Please log in.")
            except Exception as e:
                st.error(str(e))

def logout():
    clear_session()
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.active_page = "Home"
    st.success("Logged out!")
    st.rerun()

# --- MAIN LOGIC ---
if st.session_state.token and validate_session(st.session_state.token):
    st.sidebar.markdown(f"👤 **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        logout()

    st.sidebar.markdown("---")

    # Sidebar Navigation
    page = st.sidebar.radio(
        "📍 Navigate",
        ["Home", "Dashboard", "Chatbot", "Profile", "API Settings"],
        index=["Home", "Dashboard", "Chatbot", "Profile", "API Settings"].index(st.session_state.active_page),
    )
    st.session_state.active_page = page

    # --- Handle Pages ---
    if page == "Home":
        st.title("🏠 Welcome to FinWise")
        st.markdown(
            """
            FinWise is your AI-powered personal financial assistant.  
            Use the sidebar to explore:
            - **Dashboard:** Analyze and visualize your transactions  
            - **Chatbot:** Talk to your AI finance assistant  
            - **Profile:** View monthly summaries  
            - **API Settings:** Configure Groq/OpenAI keys
            """
        )

    elif page == "Dashboard":
        st.switch_page("pages/1_Dashboard.py")

    elif page == "Chatbot":
        st.switch_page("pages/2_Chatbot.py")

    elif page == "Profile":
        st.switch_page("pages/3_Profile.py")

    elif page == "API Settings":
        st.title("🔑 API Key Settings")
        st.markdown("You can configure your API keys here. These are stored securely in session memory.")

        openai_key = st.text_input("Enter OpenAI API Key", type="password", value=st.session_state.get("OPENAI_API_KEY", ""))
        groq_key = st.text_input("Enter Groq API Key", type="password", value=st.session_state.get("GROQ_API_KEY", ""))

        if st.button("💾 Save Keys"):
            st.session_state["OPENAI_API_KEY"] = openai_key
            st.session_state["GROQ_API_KEY"] = groq_key
            os.environ["OPENAI_API_KEY"] = openai_key
            os.environ["GROQ_API_KEY"] = groq_key
            st.success("✅ API keys saved successfully!")

else:
    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])
    with tab1:
        login_ui()
    with tab2:
        signup_ui()
