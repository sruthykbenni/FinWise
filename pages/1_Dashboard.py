# pages/1_Dashboard.py
import streamlit as st
from utils.session_manager import validate_session, get_user
from utils.preprocessing import load_transactions_from_csv, normalize_and_categorize
from utils.analysis import monthly_spend, category_breakdown, top_merchants
from utils.plotly_charts import monthly_spend_figure, category_pie, top_merchants_bar
from utils.rag_setup import get_rag_index
import pandas as pd
from pathlib import Path


# ---------------- Page Config ----------------
st.set_page_config(page_title="Dashboard — FinWise", layout="wide")

# ---------------- Session Validation ----------------
token = st.session_state.get("token")
if not (token and validate_session(token)):
    st.warning("Please login first.")
    st.stop()

username = get_user(token)
st.sidebar.success(f"Welcome, {username} 👋")

st.title("💰 Financial Dashboard")

st.markdown(f"""
<div style='padding:15px;border-radius:10px;margin-bottom:20px;border:1px solid #ccc;'>
<h4>👋 Welcome back, {username}!</h4>
<p>Here’s an overview of your spending habits and AI-generated insights from your transactions.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- Data Upload Section ----------------
uploaded = st.file_uploader("📂 Upload your transaction CSV", type=["csv"])

if uploaded:
    df = load_transactions_from_csv(uploaded)
    df = normalize_and_categorize(df)
    st.session_state.df = df
    st.success(f"✅ {len(df)} transactions loaded successfully.")
else:
    # Load sample data if none uploaded
    if "df" not in st.session_state:
        if st.button("Load sample data"):
            sample_path = Path("data/sample_transactions.csv")
            if sample_path.exists():
                df = load_transactions_from_csv(sample_path)
            else:
                df = pd.DataFrame({
                    "Date": pd.to_datetime(["2025-09-01", "2025-09-02", "2025-09-05", "2025-09-07"]),
                    "Description": ["Supermarket ABC", "Uber Trip", "Salary ACME", "Restaurant XYZ"],
                    "Amount": [45.12, 12.5, 2500.0, 30.0],
                    "Category": ["Grocery", "Transport", "Income", "Dining"]
                })
            df = normalize_and_categorize(df)
            st.session_state.df = df
            st.success("✅ Sample data loaded successfully.")

# ---------------- Dashboard Visualizations ----------------
if "df" in st.session_state:
    df = st.session_state.df
    st.dataframe(df.head(20), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        ms = monthly_spend(df)
        st.plotly_chart(monthly_spend_figure(ms), use_container_width=True)
    with col2:
        cat = category_breakdown(df)
        st.plotly_chart(category_pie(cat), use_container_width=True)

    st.subheader("🏪 Top Merchants")
    st.plotly_chart(top_merchants_bar(top_merchants(df, 10)), use_container_width=True)

    # ---------------- RAG Ingestion ----------------
    st.subheader("🤖 Enable Personalized Chatbot Insights")

    if st.button("Index My Transactions for Chatbot"):
        try:
            rag = get_rag_index()
            n = rag.ingest_transactions(df)
            if n > 0:
                st.success(f"✅ {n} transaction summaries indexed successfully!")
                st.info("Now visit the **Chatbot** page and ask personalized questions like:")
                st.code("What were my biggest expenses last month?")
                st.code("How can I reduce my transport costs?")
                st.code("Summarize my entertainment spending this month.")
            else:
                st.warning("No new transactions were added to the index.")
        except Exception as e:
            st.error(f"⚠️ Indexing failed: {e}")

else:
    st.info("📈 Upload or load sample data to view analytics.")

