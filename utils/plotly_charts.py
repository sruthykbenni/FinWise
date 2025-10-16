# utils/plotly_charts.py
import plotly.express as px
import pandas as pd

def monthly_spend_figure(monthly_series):
    df = pd.DataFrame({'Month': monthly_series.index.astype(str), 'Amount': monthly_series.values})
    fig = px.line(df, x='Month', y='Amount', title="Monthly Spend", markers=True)
    fig.update_layout(xaxis_title='Month', yaxis_title='Amount', template='plotly_white')
    return fig

def category_pie(df_category):
    df = df_category.reset_index().rename(columns={0:'Amount'}) if df_category.dtype == 'object' else df_category.reset_index(name='Amount')
    fig = px.pie(df, names='Category', values='Amount', title='Spending by Category')
    return fig

def top_merchants_bar(series):
    df = series.reset_index().rename(columns={0:'Amount', 'index':'Merchant'}) if series.dtype == 'object' else series.reset_index(name='Amount').rename(columns={'Description':'Merchant'})
    fig = px.bar(df, x='Amount', y=df.columns[0], orientation='h', title='Top Merchants')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig
