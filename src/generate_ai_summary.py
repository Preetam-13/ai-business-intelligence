import json
import os
from pathlib import Path
from openai import OpenAI


# --------------------------------------------------
# File paths
# --------------------------------------------------

INPUT_FILE = Path("data/processed/business_drivers.json")
OUTPUT_FILE = Path("data/processed/ai_executive_summary.txt")


# --------------------------------------------------
# Check API key
# --------------------------------------------------

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set. "
        "Set it in PowerShell before running this script."
    )


# --------------------------------------------------
# OpenRouter client
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


# --------------------------------------------------
# Load verified analytics
# --------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)


# --------------------------------------------------
# Create AI prompt
# --------------------------------------------------

prompt = f"""
You are an executive business intelligence analyst.

Create a concise executive summary from the VERIFIED business
metrics below.

IMPORTANT RULES:
1. Use ONLY the provided metrics.
2. Do not invent numbers, causes, trends, or business facts.
3. Do not claim causation unless the provided data explicitly supports it.
4. Clearly distinguish observations from recommendations.
5. Mention important risks or areas requiring attention.
6. Keep the language professional and suitable for senior management.
7. Use INR when referring to Indian currency.
8. Do not mention that the data is synthetic.

VERIFIED BUSINESS METRICS
==========================

Overall Performance:
- Total Revenue: INR {data["overall"]["total_revenue"]:,.2f}
- Total Gross Profit: INR {data["overall"]["total_gross_profit"]:,.2f}
- Gross Margin: {data["overall"]["gross_margin"]}%

Revenue Growth:
- 2023 Revenue: INR {data["revenue_growth"]["revenue_2023"]:,.2f}
- 2024 Revenue: INR {data["revenue_growth"]["revenue_2024"]:,.2f}
- 2025 Revenue: INR {data["revenue_growth"]["revenue_2025"]:,.2f}
- 2024 YoY Growth: {data["revenue_growth"]["yoy_growth_2024"]}%
- 2025 YoY Growth: {data["revenue_growth"]["yoy_growth_2025"]}%

Highest Revenue Month:
- {data["revenue_growth"]["highest_revenue_month"]["month"]}
- Revenue: INR {float(data["revenue_growth"]["highest_revenue_month"]["revenue"]):,.2f}

Lowest Revenue Month:
- {data["revenue_growth"]["lowest_revenue_month"]["month"]}
- Revenue: INR {float(data["revenue_growth"]["lowest_revenue_month"]["revenue"]):,.2f}

Category Performance:
- Highest Revenue Category:
  {data["category_analysis"]["highest_revenue_category"]["category"]}
  Revenue: INR {float(data["category_analysis"]["highest_revenue_category"]["revenue"]):,.2f}
  Margin: {data["category_analysis"]["highest_revenue_category"]["margin"]}%

- Highest Margin Category:
  {data["category_analysis"]["highest_margin_category"]["category"]}
  Margin: {data["category_analysis"]["highest_margin_category"]["margin"]}%

- Lowest Margin Category:
  {data["category_analysis"]["lowest_margin_category"]["category"]}
  Margin: {data["category_analysis"]["lowest_margin_category"]["margin"]}%

Regional Performance:
- Highest Revenue Region:
  {data["regional_analysis"]["highest_revenue_region"]["region"]}
  Revenue: INR {float(data["regional_analysis"]["highest_revenue_region"]["revenue"]):,.2f}

- Highest Margin Region:
  {data["regional_analysis"]["highest_margin_region"]["region"]}
  Margin: {data["regional_analysis"]["highest_margin_region"]["margin"]}%

- Lowest Margin Region:
  {data["regional_analysis"]["lowest_margin_region"]["region"]}
  Margin: {data["regional_analysis"]["lowest_margin_region"]["margin"]}%

Sales Channel:
- Highest Revenue Channel:
  {data["channel_analysis"]["highest_revenue_channel"]["sales_channel"]}
  Revenue: INR {float(data["channel_analysis"]["highest_revenue_channel"]["revenue"]):,.2f}

- Highest Margin Channel:
  {data["channel_analysis"]["highest_margin_channel"]["sales_channel"]}
  Margin: {data["channel_analysis"]["highest_margin_channel"]["margin"]}%

- Lowest Margin Channel:
  {data["channel_analysis"]["lowest_margin_channel"]["sales_channel"]}
  Margin: {data["channel_analysis"]["lowest_margin_channel"]["margin"]}%

Product Performance:
- Highest Revenue Product:
  {data["product_analysis"]["highest_revenue_product"]["product_name"]}
  Revenue: INR {float(data["product_analysis"]["highest_revenue_product"]["revenue"]):,.2f}
  Margin: {data["product_analysis"]["highest_revenue_product"]["margin"]}%

- Highest Gross Profit Product:
  {data["product_analysis"]["highest_profit_product"]["product_name"]}
  Gross Profit: INR {float(data["product_analysis"]["highest_profit_product"]["gross_profit"]):,.2f}
  Margin: {data["product_analysis"]["highest_profit_product"]["margin"]}%

- Lowest Margin Product Among Top Revenue Products:
  {data["product_analysis"]["lowest_margin_top_product"]["product_name"]}
  Margin: {data["product_analysis"]["lowest_margin_top_product"]["margin"]}%

Customer Retention:
- Repeat Customer Rate: {data["customer_analysis"]["repeat_customer_rate"]}%
- One-Time Customer Rate: {data["customer_analysis"]["one_time_customer_rate"]}%
- Repeat Customers: {data["customer_analysis"]["repeat_customers"]}
- One-Time Customers: {data["customer_analysis"]["one_time_customers"]}


OUTPUT FORMAT
=============

Executive Summary
Write one concise paragraph.

Key Insights
- 4 to 6 bullet points.

Areas to Monitor
- 2 to 3 bullet points.

Recommended Actions
- 2 to 3 practical recommendations.
- Clearly label them as recommendations.
"""


# --------------------------------------------------
# Call OpenRouter
# --------------------------------------------------

response = client.chat.completions.create(
    model="qwen/qwen3.8-27b:free",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a precise business intelligence analyst. "
                "Never invent metrics or unsupported facts."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)


# --------------------------------------------------
# Extract AI response
# --------------------------------------------------

summary = response.choices[0].message.content


# --------------------------------------------------
# Save AI-generated summary
# --------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(summary)


print("AI executive summary generated successfully.")
print(f"Saved to: {OUTPUT_FILE}")
print("\n" + summary)