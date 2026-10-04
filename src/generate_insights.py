import json
from sqlalchemy import create_engine, text


# PostgreSQL connection
DATABASE_URL = (
    "postgresql+psycopg2://urluser:urlpassword"
    "@localhost:5432/ai_business_intelligence"
)

engine = create_engine(DATABASE_URL)


def run_query(query):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return [dict(row._mapping) for row in result]


# --------------------------------------------------
# 1. Overall business performance
# --------------------------------------------------

overall = run_query("""
    SELECT
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS purchasing_customers,
        SUM(oi.net_revenue) AS total_revenue,
        SUM(oi.gross_profit) AS total_gross_profit,
        ROUND(
            SUM(oi.gross_profit) / NULLIF(SUM(oi.net_revenue), 0) * 100,
            2
        ) AS gross_margin
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id;
""")


# --------------------------------------------------
# 2. Monthly revenue
# --------------------------------------------------

monthly_revenue = run_query("""
    SELECT
        DATE_TRUNC('month', o.order_date)::date AS month,
        ROUND(SUM(oi.net_revenue), 2) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY 1
    ORDER BY 1;
""")


# --------------------------------------------------
# 3. Category performance
# --------------------------------------------------

category_performance = run_query("""
    SELECT
        p.category,
        ROUND(SUM(oi.net_revenue), 2) AS revenue,
        ROUND(SUM(oi.gross_profit), 2) AS gross_profit,
        ROUND(
            SUM(oi.gross_profit)
            / NULLIF(SUM(oi.net_revenue), 0) * 100,
            2
        ) AS margin
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.category
    ORDER BY revenue DESC;
""")


# --------------------------------------------------
# 4. Regional performance
# --------------------------------------------------

regional_performance = run_query("""
    SELECT
        o.region,
        ROUND(SUM(oi.net_revenue), 2) AS revenue,
        ROUND(SUM(oi.gross_profit), 2) AS gross_profit,
        ROUND(
            SUM(oi.gross_profit)
            / NULLIF(SUM(oi.net_revenue), 0) * 100,
            2
        ) AS margin
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.region
    ORDER BY revenue DESC;
""")


# --------------------------------------------------
# 5. Sales channel performance
# --------------------------------------------------

channel_performance = run_query("""
    SELECT
        o.sales_channel,
        ROUND(SUM(oi.net_revenue), 2) AS revenue,
        ROUND(SUM(oi.gross_profit), 2) AS gross_profit,
        ROUND(SUM(oi.discount_amount), 2) AS discounts,
        ROUND(
            SUM(oi.gross_profit)
            / NULLIF(SUM(oi.net_revenue), 0) * 100,
            2
        ) AS margin
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.sales_channel
    ORDER BY revenue DESC;
""")


# --------------------------------------------------
# 6. Top products
# --------------------------------------------------

top_products = run_query("""
    SELECT
        p.product_name,
        p.category,
        ROUND(SUM(oi.net_revenue), 2) AS revenue,
        ROUND(SUM(oi.gross_profit), 2) AS gross_profit,
        ROUND(
            SUM(oi.gross_profit)
            / NULLIF(SUM(oi.net_revenue), 0) * 100,
            2
        ) AS margin
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
    ORDER BY revenue DESC
    LIMIT 10;
""")

top_profit_products = run_query("""
    SELECT
        p.product_name,
        p.category,
        ROUND(SUM(oi.net_revenue), 2) AS revenue,
        ROUND(SUM(oi.gross_profit), 2) AS gross_profit,
        ROUND(
            SUM(oi.gross_profit)
            / NULLIF(SUM(oi.net_revenue), 0) * 100,
            2
        ) AS margin
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
    ORDER BY gross_profit DESC
    LIMIT 10;
""")


# --------------------------------------------------
# 7. Customer retention
# --------------------------------------------------

customer_retention = run_query("""
    WITH customer_orders AS (
        SELECT
            customer_id,
            COUNT(DISTINCT order_id) AS order_count
        FROM orders
        GROUP BY customer_id
    )
    SELECT
        COUNT(*) FILTER (WHERE order_count = 1) AS one_time_customers,
        COUNT(*) FILTER (WHERE order_count > 1) AS repeat_customers,
        COUNT(*) AS purchasing_customers,
        ROUND(
            COUNT(*) FILTER (WHERE order_count > 1)::numeric
            / NULLIF(COUNT(*), 0) * 100,
            2
        ) AS repeat_customer_rate
    FROM customer_orders;
""")


# --------------------------------------------------
# Combine results
# --------------------------------------------------

insights_data = {
    "overall": overall[0],
    "monthly_revenue": monthly_revenue,
    "category_performance": category_performance,
    "regional_performance": regional_performance,
    "channel_performance": channel_performance,
    "top_products": top_products,
    "top_profit_products": top_profit_products,
    "customer_retention": customer_retention[0],
}

# --------------------------------------------------
# Save structured output
# --------------------------------------------------

output_path = "data/processed/executive_insights.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(
        insights_data,
        file,
        indent=4,
        default=str
    )

print(f"Executive insights generated successfully.")
print(f"Saved to: {output_path}")