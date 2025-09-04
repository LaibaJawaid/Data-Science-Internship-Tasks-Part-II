import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("superstore.csv")
df.columns = df.columns.str.strip()
df['Order.Date'] = pd.to_datetime(df['Order.Date'])
df['Ship.Date'] = pd.to_datetime(df['Ship.Date'])
df = df.drop_duplicates()

# Sidebar filters
st.sidebar.header("🔎 Filters")
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
st.title("📊 Global Superstore Business Intelligence Dashboard")

# KPIs with better design
st.markdown("### 🚀 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${filtered['Sales'].sum():,.0f}")
col2.metric("📈 Total Profit", f"${filtered['Profit'].sum():,.0f}")
col3.metric("👥 Unique Customers", filtered['Customer.Name'].nunique())

# --- Chart 1: Top 5 Customers
top_customers = (
    filtered.groupby("Customer.Name")['Sales'].sum()
    .sort_values(ascending=False).head(5)
)
fig_customers = px.bar(
    top_customers,
    x=top_customers.values,
    y=top_customers.index,
    orientation='h',
    title="🏆 Top 5 Customers by Sales",
    color=top_customers.values,
    color_continuous_scale="Blues"
)
fig_customers.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=13),
    margin=dict(l=80, r=20, t=50, b=50)
)
st.plotly_chart(fig_customers, use_container_width=True)

# --- Chart 2: Segment-wise Performance
fig_segment = px.bar(
    filtered.groupby("Segment")[["Sales", "Profit"]].sum().reset_index(),
    x="Segment",
    y=["Sales", "Profit"],
    barmode="group",
    title="📦 Segment-wise Sales & Profit",
    color_discrete_sequence=px.colors.sequential.Viridis
)
fig_segment.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=13),
)
st.plotly_chart(fig_segment, use_container_width=True)

# --- Chart 3: Sales & Profit by Region (NEW)
region_perf = filtered.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
fig_region = go.Figure()

fig_region.add_trace(go.Bar(
    x=region_perf["Region"],
    y=region_perf["Sales"],
    name="Sales",
    marker_color="royalblue"
))
fig_region.add_trace(go.Bar(
    x=region_perf["Region"],
    y=region_perf["Profit"],
    name="Profit",
    marker_color="seagreen"
))
fig_region.update_layout(
    barmode="group",
    title="🌍 Sales & Profit by Region",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=13),
)
st.plotly_chart(fig_region, use_container_width=True)

# --- Chart 4: Time Series (Sales over Time)
sales_time = filtered.groupby("Order.Date")["Sales"].sum().reset_index()
fig_time = px.line(
    sales_time,
    x="Order.Date",
    y="Sales",
    title="⏳ Sales Trend Over Time",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=["#FF5733"]
)
fig_time.update_traces(marker=dict(size=6))
fig_time.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=13),
)
st.plotly_chart(fig_time, use_container_width=True)
