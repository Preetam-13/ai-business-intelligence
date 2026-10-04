-- ============================================================
-- Product Analytics
-- ============================================================

-- 1. Product performance
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.net_revenue) AS revenue,
    SUM(oi.gross_profit) AS gross_profit,
    ROUND(
        SUM(oi.gross_profit)
        / NULLIF(SUM(oi.net_revenue), 0) * 100,
        2
    ) AS gross_margin_pct
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category
ORDER BY revenue DESC;


-- 2. Top 10 products by revenue
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.net_revenue), 2) AS revenue,
    ROUND(SUM(oi.gross_profit), 2) AS gross_profit,
    ROUND(
        SUM(oi.gross_profit)
        / NULLIF(SUM(oi.net_revenue), 0) * 100,
        2
    ) AS gross_margin_pct
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10;


-- 3. Products with highest gross profit
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.net_revenue), 2) AS revenue,
    ROUND(SUM(oi.gross_profit), 2) AS gross_profit,
    ROUND(
        SUM(oi.gross_profit)
        / NULLIF(SUM(oi.net_revenue), 0) * 100,
        2
    ) AS gross_margin_pct
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY gross_profit DESC
LIMIT 10;


-- 4. Revenue vs margin by category
SELECT
    p.category,
    ROUND(SUM(oi.net_revenue), 2) AS revenue,
    ROUND(SUM(oi.gross_profit), 2) AS gross_profit,
    ROUND(
        SUM(oi.gross_profit)
        / NULLIF(SUM(oi.net_revenue), 0) * 100,
        2
    ) AS gross_margin_pct
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC;


-- 5. Discount impact by category
SELECT
    p.category,
    ROUND(SUM(oi.gross_revenue), 2) AS gross_revenue,
    ROUND(SUM(oi.discount_amount), 2) AS discount_amount,
    ROUND(SUM(oi.net_revenue), 2) AS net_revenue,
    ROUND(
        SUM(oi.discount_amount)
        / NULLIF(SUM(oi.gross_revenue), 0) * 100,
        2
    ) AS discount_pct
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY discount_pct DESC;