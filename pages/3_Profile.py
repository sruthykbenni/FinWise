# pages/3_Profile.py
import streamlit as st
from utils.session_manager import validate_session, get_user
from utils.analysis import monthly_spend, category_breakdown
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Profile — FinWise", layout="wide")

# -------------------------------------------------------------
# 🧾 Authentication
# -------------------------------------------------------------
token = st.session_state.get("token")
if not (token and validate_session(token)):
    st.warning("Please login first.")
    st.stop()

username = get_user(token)
st.sidebar.success(f"Profile — {username}")
st.title("👤 Profile & Reports")

# -------------------------------------------------------------
# 📊 Data Section
# -------------------------------------------------------------
if "df" not in st.session_state:
    st.info("Load your data from Dashboard first.")
else:
    df = st.session_state.df
    total = df["Amount"].sum()
    cat = category_breakdown(df)
    st.metric("Net Flow", f"₹{total:,.2f}")
    st.write("### Category breakdown")
    st.table(cat)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "transactions.csv", "text/csv")

    # -------------------------------------------------------------
    # 📅 Monthly Income, Expense & Net Flow Overview
    # -------------------------------------------------------------
    st.markdown("---")
    st.subheader("📆 Monthly Income & Expense Overview")

    # Ensure Date is datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    months = sorted(df["Month"].unique(), reverse=True)
    selected_month = st.selectbox("Select Month", months, index=0)

    month_df = df[df["Month"] == selected_month].copy()

    # --------------------------------------------------------------------
    # 💰 Intelligent Income, Expense & Net Flow Detection (Advanced)
    # --------------------------------------------------------------------
    month_df["Description"] = month_df["Description"].astype(str).str.lower()
    month_df["Category"] = month_df["Category"].astype(str).str.lower()

    # Income detection keywords
    income_keywords = ["salary", "income", "credit", "deposit", "refund", "bonus", "payroll", "reversal"]
    is_income = month_df["Description"].str.contains("|".join(income_keywords), case=False, na=False) | \
                month_df["Category"].str.contains("|".join(income_keywords), case=False, na=False)

    # Case 1: All amounts are positive (unsigned data)
    if (month_df["Amount"] >= 0).all():
        # If no rows matched as income, assume largest values are likely income
        if is_income.sum() == 0:
            threshold = month_df["Amount"].quantile(0.9)  # top 10% values
            is_income = month_df["Amount"] >= threshold

        income = month_df.loc[is_income, "Amount"].sum()
        expense = month_df.loc[~is_income, "Amount"].sum()
        expense = -abs(expense)
        netflow = income + expense

    # Case 2: Signed amounts (positive = income, negative = expense)
    else:
        income = month_df.loc[month_df["Amount"] > 0, "Amount"].sum()
        expense = month_df.loc[month_df["Amount"] < 0, "Amount"].sum()
        netflow = income + expense


    # -------------------------------------------------------------
    # 📈 Display Metrics and Visualization
    # -------------------------------------------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Income", f"₹{income:,.2f}")
    col2.metric("💸 Expense", f"₹{abs(expense):,.2f}")
    col3.metric(
        "⚖️ Net Flow",
        f"₹{netflow:,.2f}",
        delta=f"{'+' if netflow >= 0 else ''}{netflow:,.2f}",
        delta_color="normal" if netflow >= 0 else "inverse",
    )

    # 📊 Income vs Expense Bar Chart
    fig = go.Figure()
    fig.add_bar(name="Income", x=[selected_month], y=[income], marker_color="green")
    fig.add_bar(name="Expense", x=[selected_month], y=[abs(expense)], marker_color="red")
    fig.update_layout(
        barmode="group",
        title=f"Income vs Expense — {selected_month}",
        yaxis_title="Amount (₹)",
        xaxis_title="Month",
        showlegend=True,
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------
    # 🧭 Optional Net Flow Summary Table
    # -------------------------------------------------------------
    st.markdown("### 🧾 Summary for Selected Month")
    summary_df = pd.DataFrame({
        "Metric": ["Income", "Expense", "Net Flow"],
        "Amount (₹)": [f"{income:,.2f}", f"{abs(expense):,.2f}", f"{netflow:,.2f}"]
    })
    st.table(summary_df)
