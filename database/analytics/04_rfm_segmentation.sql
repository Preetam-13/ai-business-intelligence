-- RFM Customer Segmentation

WITH customer_rfm AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.region,
        c.customer_segment AS business_segment,
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
        c.customer_name,
        c.region,
        c.customer_segment
),

rfm_scores AS (
    SELECT
        *,
        DATE '2026-01-01' - last_order_date AS recency_days,

        NTILE(5) OVER (
            ORDER BY last_order_date DESC
        ) AS r_score,

        NTILE(5) OVER (
            ORDER BY frequency ASC
        ) AS f_score,

        NTILE(5) OVER (
            ORDER BY monetary ASC
        ) AS m_score
    FROM customer_rfm
),

rfm_segments AS (
    SELECT
        *,
        r_score + f_score + m_score AS rfm_score,
        CASE
            WHEN r_score >= 4
                 AND f_score >= 4
                 AND m_score >= 4
                THEN 'High Value'

            WHEN r_score >= 4
                 AND f_score >= 3
                THEN 'Loyal'

            WHEN r_score <= 2
                 AND f_score >= 3
                THEN 'At Risk'

            WHEN r_score >= 4
                 AND f_score <= 2
                THEN 'New / Promising'

            ELSE 'Regular'
        END AS rfm_segment
    FROM rfm_scores
)

SELECT
    rfm_segment,
    COUNT(*) AS customers,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage,
    ROUND(AVG(monetary), 2) AS avg_customer_revenue,
    ROUND(AVG(frequency), 2) AS avg_order_frequency
FROM rfm_segments
GROUP BY rfm_segment
ORDER BY customers DESC;