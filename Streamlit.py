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

# KPIs
st.markdown("### 🚀 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${filtered['Sales'].sum():,.0f}")
col2.metric("📈 Total Profit", f"${filtered['Profit'].sum():,.0f}")
col3.metric("👥 Unique Customers", filtered['Customer.Name'].nunique())

# --- Add spacing before charts
st.markdown("---")
st.markdown("## 📊 Visual Insights")
st.markdown(" ")  # extra gap

# Function to apply professional style to all charts
def style_chart(fig, title, x_title=None, y_title=None):
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="black", family="Arial Black")),
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=14, color="black", family="Arial Black")),
            tickfont=dict(size=12, color="black", family="Arial Black")
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=14, color="black", family="Arial Black")),
            tickfont=dict(size=12, color="black", family="Arial Black")
        ),
        legend=dict(
            font=dict(size=12, color="black", family="Arial Black")
        ),
        coloraxis_colorbar=dict(
            title=dict(font=dict(size=12, color="black", family="Arial Black")),
            tickfont=dict(size=12, color="black", family="Arial Black")
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    return fig


# --- Chart 1: Top 5 Customers
st.markdown("### 🏆 Top 5 Customers by Sales")
top_customers = (
    filtered.groupby("Customer.Name")['Sales'].sum()
    .sort_values(ascending=False).head(5)
)
fig_customers = px.bar(
    top_customers,
    x=top_customers.values,
    y=top_customers.index,
    orientation='h',
    color=top_customers.values,
    color_continuous_scale="Blues"
)
fig_customers = style_chart(fig_customers, "Top 5 Customers by Sales", x_title="Sales", y_title="Customer Name")
st.plotly_chart(fig_customers, use_container_width=True)

st.markdown(" ")  # gap


# --- Chart 2: Segment-wise Performance
st.markdown("### 📦 Segment-wise Sales & Profit")
fig_segment = px.bar(
    filtered.groupby("Segment")[["Sales", "Profit"]].sum().reset_index(),
    x="Segment",
    y=["Sales", "Profit"],
    barmode="group",
    color_discrete_sequence=px.colors.sequential.Viridis
)
fig_segment = style_chart(fig_segment, "Segment-wise Sales & Profit", x_title="Segment", y_title="Value")
st.plotly_chart(fig_segment, use_container_width=True)

st.markdown(" ")  # gap


# --- Chart 3: Sales & Profit by Region
st.markdown("### 🌍 Sales & Profit by Region")
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
fig_region = style_chart(fig_region, "Sales & Profit by Region", x_title="Region", y_title="Value")
st.plotly_chart(fig_region, use_container_width=True)

st.markdown(" ")  # gap


# --- Chart 4: Sales Trend Over Time
st.markdown("### ⏳ Sales Trend Over Time")
sales_time = filtered.groupby("Order.Date")["Sales"].sum().reset_index()
fig_time = px.line(
    sales_time,
    x="Order.Date",
    y="Sales",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=["#FF5733"]
)
fig_time.update_traces(marker=dict(size=6))
fig_time = style_chart(fig_time, "Sales Trend Over Time", x_title="Order_Date", y_title="Sales")
st.plotly_chart(fig_time, use_container_width=True)
