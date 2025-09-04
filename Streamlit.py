import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("superstore.csv")
df.columns = df.columns.str.strip()
df['Order.Date'] = pd.to_datetime(df['Order.Date'])
df['Ship.Date'] = pd.to_datetime(df['Ship.Date'])
df = df.drop_duplicates()

# Sidebar filters
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Select Region", df['Region'].unique())
category = st.sidebar.multiselect("Select Category", df['Category'].unique())
sub_category = st.sidebar.multiselect("Select Sub-Category", df['Sub.Category'].unique())

# Apply filters
filtered = df.copy()
if region:
    filtered = filtered[filtered['Region'].isin(region)]
if category:
    filtered = filtered[filtered['Category'].isin(category)]
if sub_category:
    filtered = filtered[filtered['Sub.Category'].isin(sub_category)]

# Title
st.title("📊 Global Superstore Dashboard")

# KPIs
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")

# Top 5 Customers
top_customers = (
    filtered.groupby("Customer.Name")['Sales'].sum()   # ✅ Correct column name
    .sort_values(ascending=False).head(5)
)
fig_customers = px.bar(
    top_customers,
    x=top_customers.values,
    y=top_customers.index,
    orientation='h',
    title="Top 5 Customers by Sales"
)
st.plotly_chart(fig_customers)

# Segment-wise Performance
fig_segment = px.bar(
    filtered.groupby("Segment")[["Sales","Profit"]].sum().reset_index(),
    x="Segment",
    y=["Sales","Profit"],
    barmode="group",
    title="Segment-wise Sales & Profit"
)
st.plotly_chart(fig_segment)
