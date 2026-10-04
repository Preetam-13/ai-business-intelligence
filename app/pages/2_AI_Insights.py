import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="AI Executive Insights",
    page_icon="🤖",
    layout="wide"
)

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

DRIVERS_FILE = BASE_DIR / "data" / "processed" / "business_drivers.json"
SUMMARY_FILE = BASE_DIR / "data" / "processed" / "ai_executive_summary.txt"

# Load data
with open(DRIVERS_FILE, "r", encoding="utf-8") as f:
    drivers = json.load(f)

with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
    ai_summary = f.read()

# Extract sections from the actual JSON
overall = drivers["overall"]
growth = drivers["revenue_growth"]
category = drivers["category_analysis"]
regional = drivers["regional_analysis"]
channel = drivers["channel_analysis"]
product = drivers["product_analysis"]
customer = drivers["customer_analysis"]

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 AI Executive Insights")

st.caption(
    "AI-generated business analysis based on verified "
    "revenue, profitability, product, regional, channel "
    "and customer metrics."
)

st.divider()

# --------------------------------------------------
# AI Summary
# --------------------------------------------------

st.subheader("🧠 Executive Summary")

st.markdown(
    f"""
    <div style="
        background-color: #16263A;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #263B55;
        line-height: 1.7;
        font-size: 16px;
    ">
        {ai_summary.replace(chr(10), '<br>')}
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Key Business Drivers
# --------------------------------------------------

st.subheader("📊 Key Business Drivers")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Top Category",
        category["highest_revenue_category"]["category"]
    )

with col2:
    st.metric(
        "Top Region",
        regional["highest_revenue_region"]["region"]
    )

with col3:
    st.metric(
        "Repeat Customers",
        f"{customer['repeat_customer_rate']:.2f}%"
    )

# --------------------------------------------------
# Category Analysis
# --------------------------------------------------

st.divider()

st.subheader("🏷️ Category Analysis")

highest_category = category["highest_revenue_category"]

col1, col2 = st.columns(2)

with col1:
    st.write("**Highest Revenue Category**")
    st.write(highest_category["category"])

    st.write("**Revenue**")
    st.write(
        f"₹{float(highest_category['revenue']):,.0f}"
    )

with col2:
    st.write("**Revenue Share**")
    st.write(
        f"{category['revenue_share_by_category'][highest_category['category']]:.2f}%"
    )

    st.write("**Gross Margin**")
    st.write(
        f"{float(highest_category['margin']):.2f}%"
    )

# --------------------------------------------------
# Regional Analysis
# --------------------------------------------------

st.subheader("🌎 Regional Analysis")

col1, col2 = st.columns(2)

with col1:
    highest_region = regional["highest_revenue_region"]

    st.write("**Highest Revenue Region**")
    st.write(highest_region["region"])

    st.write(
        f"Revenue: ₹{float(highest_region['revenue']):,.0f}"
    )

with col2:
    highest_region_margin = regional["highest_margin_region"]

    st.write("**Highest Regional Margin**")
    st.write(highest_region_margin["region"])

    st.write(
        f"Margin: {float(highest_region_margin['margin']):.2f}%"
    )

# --------------------------------------------------
# Sales Channel Analysis
# --------------------------------------------------

st.divider()

st.subheader("🛒 Sales Channel Analysis")

highest_channel = channel["highest_revenue_channel"]
lowest_margin_channel = channel["lowest_margin_channel"]

col1, col2 = st.columns(2)

with col1:
    st.write("**Highest Revenue Channel**")
    st.write(
        highest_channel["sales_channel"]
    )

    st.write(
        f"Revenue: ₹{float(highest_channel['revenue']):,.0f}"
    )

with col2:
    st.write("**Lowest Margin Channel**")
    st.write(
        lowest_margin_channel["sales_channel"]
    )

    st.write(
        f"Margin: {float(lowest_margin_channel['margin']):.2f}%"
    )

# --------------------------------------------------
# Product Analysis
# --------------------------------------------------

st.subheader("📦 Product Analysis")

highest_revenue_product = product["highest_revenue_product"]
highest_profit_product = product["highest_profit_product"]
lowest_margin_product = product["lowest_margin_top_product"]

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Highest Revenue Product**")
    st.write(highest_revenue_product["product_name"])
    st.write(
        f"Revenue: ₹{float(highest_revenue_product['revenue']):,.0f}"
    )

with col2:
    st.write("**Highest Profit Product**")
    st.write(highest_profit_product["product_name"])
    st.write(
        f"Gross Profit: ₹{float(highest_profit_product['gross_profit']):,.0f}"
    )

with col3:
    st.write("**Lowest Margin Top-Revenue Product**")
    st.write(lowest_margin_product["product_name"])
    st.write(
        f"Margin: {float(lowest_margin_product['margin']):.2f}%"
    )

# --------------------------------------------------
# Customer Analysis
# --------------------------------------------------

st.divider()

st.subheader("👥 Customer Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Repeat Customers",
        f"{customer['repeat_customers']:,}"
    )

with col2:
    st.metric(
        "One-Time Customers",
        f"{customer['one_time_customers']:,}"
    )

with col3:
    st.metric(
        "Repeat Customer Rate",
        f"{customer['repeat_customer_rate']:.2f}%"
    )

# --------------------------------------------------
# Revenue Trend
# --------------------------------------------------

st.divider()

st.subheader("📈 Revenue Trend Drivers")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Highest Revenue Month",
        growth["highest_revenue_month"]["month"]
    )

    st.write(
        f"Revenue: ₹"
        f"{float(growth['highest_revenue_month']['revenue']):,.0f}"
    )

with col2:
    st.metric(
        "Lowest Revenue Month",
        growth["lowest_revenue_month"]["month"]
    )

    st.write(
        f"Revenue: ₹"
        f"{float(growth['lowest_revenue_month']['revenue']):,.0f}"
    )

# --------------------------------------------------
# Methodology
# --------------------------------------------------

st.divider()

with st.expander("ℹ️ About these insights"):
    st.write(
        """
        The AI insights are generated from metrics calculated
        by the Python analytics pipeline.

        PostgreSQL and Python calculate the underlying business
        metrics first. The AI layer then converts these verified
        metrics into an executive-friendly narrative.

        AI is not responsible for calculating the underlying
        revenue, profit, customer or product metrics.
        """
    )

st.caption(
    "NovaMart Analytics • Synthetic dataset • Jan 2023 – Dec 2025"
)