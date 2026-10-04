import json
from pathlib import Path


INPUT_FILE = Path("data/processed/executive_insights.json")
OUTPUT_FILE = Path("data/processed/business_drivers.json")


# --------------------------------------------------
# Load analytics output
# --------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def to_float(value):
    return float(value)


def percentage(part, total):
    if total == 0:
        return 0
    return round((part / total) * 100, 2)


# --------------------------------------------------
# Overall metrics
# --------------------------------------------------

overall = data["overall"]

total_revenue = to_float(overall["total_revenue"])
total_profit = to_float(overall["total_gross_profit"])
gross_margin = to_float(overall["gross_margin"])


# --------------------------------------------------
# Monthly revenue analysis
# --------------------------------------------------

monthly = data["monthly_revenue"]

revenue_2023 = sum(
    to_float(x["revenue"])
    for x in monthly
    if x["month"].startswith("2023")
)

revenue_2024 = sum(
    to_float(x["revenue"])
    for x in monthly
    if x["month"].startswith("2024")
)

revenue_2025 = sum(
    to_float(x["revenue"])
    for x in monthly
    if x["month"].startswith("2025")
)


yoy_2024 = round(
    (revenue_2024 - revenue_2023) / revenue_2023 * 100,
    2
)

yoy_2025 = round(
    (revenue_2025 - revenue_2024) / revenue_2024 * 100,
    2
)


# Find highest and lowest revenue months
highest_month = max(
    monthly,
    key=lambda x: to_float(x["revenue"])
)

lowest_month = min(
    monthly,
    key=lambda x: to_float(x["revenue"])
)


# --------------------------------------------------
# Category analysis
# --------------------------------------------------

categories = data["category_performance"]

highest_category_revenue = max(
    categories,
    key=lambda x: to_float(x["revenue"])
)

highest_category_margin = max(
    categories,
    key=lambda x: to_float(x["margin"])
)

lowest_category_margin = min(
    categories,
    key=lambda x: to_float(x["margin"])
)


category_revenue_share = {
    item["category"]: percentage(
        to_float(item["revenue"]),
        total_revenue
    )
    for item in categories
}


# --------------------------------------------------
# Regional analysis
# --------------------------------------------------

regions = data["regional_performance"]

highest_region_revenue = max(
    regions,
    key=lambda x: to_float(x["revenue"])
)

highest_region_margin = max(
    regions,
    key=lambda x: to_float(x["margin"])
)

lowest_region_margin = min(
    regions,
    key=lambda x: to_float(x["margin"])
)


# --------------------------------------------------
# Sales channel analysis
# --------------------------------------------------

channels = data["channel_performance"]

highest_channel_revenue = max(
    channels,
    key=lambda x: to_float(x["revenue"])
)

highest_channel_margin = max(
    channels,
    key=lambda x: to_float(x["margin"])
)

lowest_channel_margin = min(
    channels,
    key=lambda x: to_float(x["margin"])
)


# --------------------------------------------------
# Product analysis
# --------------------------------------------------

products = data["top_products"]
profit_products = data["top_profit_products"]

highest_product_revenue = max(
    products,
    key=lambda x: to_float(x["revenue"])
)

highest_product_profit = max(
    profit_products,
    key=lambda x: to_float(x["gross_profit"])
)

lowest_margin_top_product = min(
    products,
    key=lambda x: to_float(x["margin"])
)


# --------------------------------------------------
# Customer retention analysis
# --------------------------------------------------

retention = data["customer_retention"]

repeat_customer_rate = to_float(
    retention["repeat_customer_rate"]
)

one_time_customer_rate = round(
    100 - repeat_customer_rate,
    2
)


# --------------------------------------------------
# Build structured business drivers
# --------------------------------------------------

business_drivers = {

    "overall": {
        "total_revenue": total_revenue,
        "total_gross_profit": total_profit,
        "gross_margin": gross_margin
    },

    "revenue_growth": {
        "revenue_2023": round(revenue_2023, 2),
        "revenue_2024": round(revenue_2024, 2),
        "revenue_2025": round(revenue_2025, 2),
        "yoy_growth_2024": yoy_2024,
        "yoy_growth_2025": yoy_2025,
        "highest_revenue_month": highest_month,
        "lowest_revenue_month": lowest_month
    },

    "category_analysis": {
        "highest_revenue_category": highest_category_revenue,
        "highest_margin_category": highest_category_margin,
        "lowest_margin_category": lowest_category_margin,
        "revenue_share_by_category": category_revenue_share
    },

    "regional_analysis": {
        "highest_revenue_region": highest_region_revenue,
        "highest_margin_region": highest_region_margin,
        "lowest_margin_region": lowest_region_margin
    },

    "channel_analysis": {
        "highest_revenue_channel": highest_channel_revenue,
        "highest_margin_channel": highest_channel_margin,
        "lowest_margin_channel": lowest_channel_margin
    },

    "product_analysis": {
        "highest_revenue_product": highest_product_revenue,
        "highest_profit_product": highest_product_profit,
        "lowest_margin_top_product": lowest_margin_top_product
    },

    "customer_analysis": {
        "repeat_customer_rate": repeat_customer_rate,
        "one_time_customer_rate": one_time_customer_rate,
        "repeat_customers": retention["repeat_customers"],
        "one_time_customers": retention["one_time_customers"]
    }
}


# --------------------------------------------------
# Save output
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(
        business_drivers,
        file,
        indent=4,
        default=str
    )


print("Business driver analysis completed successfully.")
print(f"Saved to: {OUTPUT_FILE}")