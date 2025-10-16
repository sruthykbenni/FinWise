# app.py
import streamlit as st
from utils.auth import init_db, verify_user, create_user
from utils.session_manager import create_session, validate_session, clear_session

st.set_page_config(page_title="FinWise", page_icon="💰", layout="wide")

init_db()

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

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
    st.success("Logged out!")
    st.rerun()

# --- Routing Logic ---
if st.session_state.token and validate_session(st.session_state.token):
    st.sidebar.markdown(f"👤 **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        logout()
    st.sidebar.markdown("---")
    st.sidebar.success("Use the sidebar to navigate.")
    st.switch_page("pages/1_Dashboard.py")
else:
    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])
    with tab1:
        login_ui()
    with tab2:
        signup_ui()
