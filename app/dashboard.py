import streamlit as st
import json
from pathlib import Path
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="NovaMart Analytics",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Load analytics data
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

with open(DATA_DIR / "executive_insights.json", "r", encoding="utf-8") as file:
    insights = json.load(file)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("NovaMart Business Intelligence")
st.caption("AI-Powered Revenue & Business Analytics Platform")

POWER_BI_URL = "https://app.powerbi.com/groups/me/reports/cc252f48-6fcb-46aa-b3fd-8cfc9d3ede13/9c0e9b0e73b7acd76a9e?experience=power-bi"

st.link_button(
    "📊 Open Power BI Dashboard",
    POWER_BI_URL,
    width="stretch"
)

# --------------------------------------------------
# Extract metrics
# --------------------------------------------------

overall = insights["overall"]

total_revenue = float(overall["total_revenue"])
total_profit = float(overall["total_gross_profit"])
gross_margin = float(overall["gross_margin"])
total_orders = int(overall["total_orders"])
purchasing_customers = int(overall["purchasing_customers"])

aov = total_revenue / total_orders


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue / 1e9:.2f}B"
    )

with col2:
    st.metric(
        "Gross Profit",
        f"₹{total_profit / 1e9:.2f}B"
    )

with col3:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col4:
    st.metric(
        "Average Order Value",
        f"₹{aov:,.0f}"
    )

with col5:
    st.metric(
        "Gross Margin",
        f"{gross_margin:.2f}%"
    )


st.divider()


# --------------------------------------------------
# Monthly Revenue
# --------------------------------------------------

st.subheader("Monthly Revenue Trend")

monthly_df = pd.DataFrame(insights["monthly_revenue"])

monthly_df["month"] = pd.to_datetime(monthly_df["month"])
monthly_df["revenue"] = monthly_df["revenue"].astype(float)

fig_monthly = px.line(
    monthly_df,
    x="month",
    y="revenue",
    markers=True,
    labels={
        "month": "Month",
        "revenue": "Revenue"
    }
)

fig_monthly.update_yaxes(
    tickprefix="₹",
    tickformat=",.0f"
)

fig_monthly.update_layout(
    height=450,
    hovermode="x unified"
)

st.plotly_chart(
    fig_monthly,
    width="stretch"
)


# --------------------------------------------------
# Category Revenue
# --------------------------------------------------

st.subheader("Revenue by Product Category")

category_df = pd.DataFrame(insights["category_performance"])

category_df["revenue"] = category_df["revenue"].astype(float)

fig_category = px.bar(
    category_df.sort_values("revenue"),
    x="revenue",
    y="category",
    orientation="h",
    labels={
        "revenue": "Revenue",
        "category": "Category"
    }
)

fig_category.update_xaxes(
    tickprefix="₹",
    tickformat=",.0f"
)

fig_category.update_layout(
    height=400
)

st.plotly_chart(
    fig_category,
    width="stretch"
)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    f"Purchasing Customers: {purchasing_customers:,} | "
    "Data period: January 2023 – December 2025"
)