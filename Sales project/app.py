import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/sersun/supermarket-sales-analysis/main/supermarket_sales.csv"
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day_name()
    return df

df = load_data()

# Title
st.title("📊 Supermarket Sales Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_branch = st.sidebar.multiselect("Select Branch", options=df['Branch'].unique(), default=df['Branch'].unique())
selected_product = st.sidebar.multiselect("Select Product Line", options=df['Product line'].unique(), default=df['Product line'].unique())

# Filter data
filtered_df = df[(df['Branch'].isin(selected_branch)) & (df['Product line'].isin(selected_product))]

# KPIs
total_sales = filtered_df['Total'].sum()
avg_rating = filtered_df['Rating'].mean()

st.metric("💰 Total Sales", f"${total_sales:,.2f}")
st.metric("⭐ Average Rating", f"{avg_rating:.2f} / 10")

# Plot 1: Sales by Product Line
st.subheader("Total Sales by Product Line")
fig1, ax1 = plt.subplots()
sns.barplot(data=filtered_df, y='Product line', x='Total', estimator=sum, ci=None, ax=ax1, palette='viridis')
st.pyplot(fig1)

# Plot 2: Monthly Sales Trend
st.subheader("Monthly Sales Trend")
monthly_sales = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Total'].sum().reset_index()
monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()
fig2, ax2 = plt.subplots()
sns.lineplot(data=monthly_sales, x='Date', y='Total', marker='o', ax=ax2)
st.pyplot(fig2)
