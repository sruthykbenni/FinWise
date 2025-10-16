import pandas as pd
import numpy as np

DEFAULT_CATEGORIES = {
    "grocery": ["store", "supermarket", "grocer"],
    "rent": ["rent"],
    "transport": ["uber", "ola", "taxi", "metro", "bus"],
    "dining": ["restaurant", "cafe", "starbucks"],
    "salary": ["salary", "payroll", "salary credit"],
}

def load_transactions_from_csv(path_or_buffer):
    """
    Load transactions from a CSV and auto-detect key columns like date, amount, etc.
    Handles variations such as 'Debit/Credit' and 'Transaction Date' columns.
    """
    df = pd.read_csv(path_or_buffer)

    # Normalize column names (case-insensitive)
    df.columns = [c.strip().title() for c in df.columns]

    # --- Detect and parse Date column ---
    date_candidates = [c for c in df.columns if "Date" in c]
    if date_candidates:
        date_col = date_candidates[0]
        df.rename(columns={date_col: "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    else:
        df["Date"] = pd.date_range(start="2025-01-01", periods=len(df))

    # --- Handle Debit/Credit or Amount ---
    if "Debit" in df.columns or "Credit" in df.columns:
        df["Debit"] = pd.to_numeric(df.get("Debit", 0), errors="coerce").fillna(0)
        df["Credit"] = pd.to_numeric(df.get("Credit", 0), errors="coerce").fillna(0)
        df["Amount"] = df["Credit"] - df["Debit"]
    elif "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    else:
        # fallback: create Amount column with zeros
        df["Amount"] = 0.0

    return df


def normalize_and_categorize(df):
    """
    Cleans transaction data by ensuring standard columns:
    Date, Description, Amount, and Category.
    Handles both Debit/Credit and Amount styles.
    """

    # Normalize column names
    df.columns = [c.strip().title() for c in df.columns]

    # --- Handle Debit/Credit logic if available ---
    if "Debit" in df.columns or "Credit" in df.columns:
        df["Debit"] = pd.to_numeric(df.get("Debit", 0), errors="coerce").fillna(0)
        df["Credit"] = pd.to_numeric(df.get("Credit", 0), errors="coerce").fillna(0)
        df["Amount"] = df["Credit"] - df["Debit"]
    elif "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    else:
        df["Amount"] = 0.0

    # --- Detect Description column ---
    desc_candidates = [c for c in df.columns if any(k in c.lower() for k in ["desc", "narration", "merchant", "details"])]
    if desc_candidates:
        df.rename(columns={desc_candidates[0]: "Description"}, inplace=True)
    elif "Description" not in df.columns:
        df["Description"] = "Unknown"

    # --- Detect or Create Date column ---
    date_candidates = [c for c in df.columns if "date" in c.lower()]
    if date_candidates:
        df.rename(columns={date_candidates[0]: "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    else:
        df["Date"] = pd.date_range(start="2025-01-01", periods=len(df))

    # --- Categorization Logic ---
    def categorize(desc):
        desc = str(desc).lower()
        if any(x in desc for x in ["salary", "deposit", "credit", "income"]):
            return "Income"
        elif any(x in desc for x in ["uber", "ola", "fuel", "bus", "train"]):
            return "Transport"
        elif any(x in desc for x in ["supermarket", "grocery", "mart", "store"]):
            return "Groceries"
        elif any(x in desc for x in ["restaurant", "food", "cafe", "hotel"]):
            return "Food & Dining"
        elif any(x in desc for x in ["netflix", "amazon", "movie", "entertainment"]):
            return "Entertainment"
        elif any(x in desc for x in ["electricity", "internet", "mobile", "bill"]):
            return "Utilities"
        else:
            return "Other"

    df["Category"] = df["Description"].apply(categorize)

    # --- Sort by Date ---
    df.sort_values("Date", inplace=True, ignore_index=True)
    return df
