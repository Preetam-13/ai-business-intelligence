-- ============================================================
-- Customer Analytics
-- ============================================================

-- 1. Customer-level performance
WITH customer_metrics AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.city,
        c.region,
        c.customer_segment,
        COUNT(DISTINCT o.order_id) AS total_orders,
        MIN(o.order_date) AS first_order_date,
        MAX(o.order_date) AS last_order_date,
        SUM(oi.net_revenue) AS total_revenue,
        SUM(oi.gross_profit) AS total_gross_profit
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id,
        c.customer_name,
        c.city,
        c.region,
        c.customer_segment
)

SELECT
    *,
    ROUND(
        total_revenue / NULLIF(total_orders, 0),
        2
    ) AS customer_aov
FROM customer_metrics
ORDER BY total_revenue DESC;


-- 2. Top 20 customers by revenue
WITH customer_metrics AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.region,
        c.customer_segment,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.net_revenue) AS total_revenue,
        SUM(oi.gross_profit) AS total_gross_profit
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id,
        c.customer_name,
        c.region,
        c.customer_segment
)

SELECT
    customer_id,
    customer_name,
    region,
    customer_segment,
    total_orders,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_gross_profit, 2) AS total_gross_profit
FROM customer_metrics
ORDER BY total_revenue DESC
LIMIT 20;


-- 3. Repeat vs one-time customers
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY customer_id
)

SELECT
    CASE
        WHEN order_count = 1 THEN 'One-Time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,
    COUNT(*) AS customers,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_pct
FROM customer_orders
GROUP BY
    CASE
        WHEN order_count = 1 THEN 'One-Time Customer'
        ELSE 'Repeat Customer'
    END;


-- 4. RFM base metrics
WITH rfm_base AS (
    SELECT
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.net_revenue) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id,
        c.customer_name
)

SELECT
    *,
    CURRENT_DATE - last_order_date AS recency_days
FROM rfm_base
ORDER BY monetary DESC;


-- 5. RFM scoring
WITH rfm_base AS (
    SELECT
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.net_revenue) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id,
        c.customer_name
),

rfm_scores AS (
    SELECT
        *,
        NTILE(5) OVER (
            ORDER BY last_order_date DESC
        ) AS recency_score,

        NTILE(5) OVER (
            ORDER BY frequency
        ) AS frequency_score,

        NTILE(5) OVER (
            ORDER BY monetary
        ) AS monetary_score
    FROM rfm_base
)

SELECT
    *,
    recency_score
        + frequency_score
        + monetary_score AS rfm_total_score
FROM rfm_scores
ORDER BY rfm_total_score DESC;


-- 6. Customer segment distribution
WITH rfm_base AS (
    SELECT
        c.customer_id,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.net_revenue) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_id
),

rfm_scores AS (
    SELECT
        *,
        NTILE(5) OVER (
            ORDER BY last_order_date DESC
        ) AS r_score,

        NTILE(5) OVER (
            ORDER BY frequency
        ) AS f_score,

        NTILE(5) OVER (
            ORDER BY monetary
        ) AS m_score
    FROM rfm_base
)

SELECT
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4
            THEN 'High Value'
        WHEN r_score >= 4 AND f_score >= 3
            THEN 'Loyal'
        WHEN r_score <= 2 AND f_score >= 3
            THEN 'At Risk'
        WHEN r_score >= 4 AND f_score <= 2
            THEN 'New / Promising'
        ELSE 'Regular'
    END AS customer_segment,
    COUNT(*) AS customers
FROM rfm_scores
GROUP BY 1
ORDER BY customers DESC;