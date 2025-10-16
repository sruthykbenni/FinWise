# utils/analysis.py
def monthly_spend(df):
    df = df.copy()
    df['ym'] = df['Date'].dt.to_period('M')
    m = df.groupby('ym')['Amount'].sum().sort_index()
    return m

def category_breakdown(df):
    return df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

def top_merchants(df, n=10):
    return df.groupby('Description')['Amount'].sum().nlargest(n)
