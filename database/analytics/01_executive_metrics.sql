-- ============================================================
-- Executive Business Metrics
-- AI Business Intelligence & Revenue Analytics Platform
-- ============================================================

-- 1. Overall business performance
SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    SUM(oi.net_revenue) AS total_revenue,
    SUM(oi.gross_profit) AS total_gross_profit,
    ROUND(
        SUM(oi.gross_profit) / NULLIF(SUM(oi.net_revenue), 0) * 100,
        2
    ) AS gross_margin_pct
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id;


-- 2. Average Order Value
SELECT
    ROUND(
        SUM(order_revenue) / COUNT(*),
        2
    ) AS average_order_value
FROM (
    SELECT
        o.order_id,
        SUM(oi.net_revenue) AS order_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.order_id
) order_totals;


-- 3. Monthly revenue trend
SELECT
    DATE_TRUNC('month', o.order_date)::DATE AS month,
    SUM(oi.net_revenue) AS revenue,
    SUM(oi.gross_profit) AS gross_profit,
    ROUND(
        SUM(oi.gross_profit)
        / NULLIF(SUM(oi.net_revenue), 0) * 100,
        2
    ) AS gross_margin_pct
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;


-- 4. Revenue by region
SELECT
    o.region,
    COUNT(DISTINCT o.order_id) AS orders,
    SUM(oi.net_revenue) AS revenue,
    SUM(oi.gross_profit) AS gross_profit,
    ROUND(
        SUM(oi.gross_profit)
        / NULLIF(SUM(oi.net_revenue), 0) * 100,
        2
    ) AS gross_margin_pct
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.region
ORDER BY revenue DESC;


-- 5. Revenue by product category
SELECT
    p.category,
    COUNT(DISTINCT o.order_id) AS orders,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.net_revenue) AS revenue,
    SUM(oi.gross_profit) AS gross_profit,
    ROUND(
        SUM(oi.gross_profit)
        / NULLIF(SUM(oi.net_revenue), 0) * 100,
        2
    ) AS gross_margin_pct
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;