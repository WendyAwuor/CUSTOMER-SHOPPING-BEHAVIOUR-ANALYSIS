/*
============================================================
RETAIL CUSTOMER INSIGHTS
SQL ANALYSIS

Database:
    retail_customer_insights

Purpose:
    Business analysis of customer shopping behaviour.

Sections:
    1. Data validation
    2. Executive KPIs
    3. Revenue by category
    4. Revenue by age group
    5. Customer segmentation
    6. Subscription analysis
    7. Discount analysis
    8. Payment method analysis
    9. Shipping analysis
    10. Seasonal analysis
    11. Top products
============================================================
*/


-- =========================================================
-- 1. CREATE TABLE
-- =========================================================

DROP TABLE IF EXISTS customer_behavior;

CREATE TABLE customer_behavior (
    customer_id INTEGER,
    age INTEGER,
    gender VARCHAR(20),
    item_purchased VARCHAR(100),
    category VARCHAR(100),
    purchase_amount NUMERIC(10,2),
    location VARCHAR(100),
    size VARCHAR(20),
    color VARCHAR(50),
    season VARCHAR(50),
    review_rating NUMERIC(3,2),
    subscription_status VARCHAR(20),
    shipping_type VARCHAR(50),
    discount_applied VARCHAR(20),
    previous_purchases INTEGER,
    payment_method VARCHAR(50),
    frequency_of_purchases VARCHAR(50),
    age_group VARCHAR(30),
    purchase_frequency_days INTEGER
);


-- =========================================================
-- 2. DATA VALIDATION
-- =========================================================

-- Total records
SELECT COUNT(*) AS total_records
FROM customer_behavior;


-- Unique customers
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM customer_behavior;


-- Missing values
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer_id,
    COUNT(*) FILTER (WHERE purchase_amount IS NULL) AS missing_purchase_amount,
    COUNT(*) FILTER (WHERE category IS NULL) AS missing_category,
    COUNT(*) FILTER (WHERE review_rating IS NULL) AS missing_review_rating
FROM customer_behavior;


-- =========================================================
-- 3. EXECUTIVE KPIs
-- =========================================================

SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(*) AS total_purchases,
    ROUND(SUM(purchase_amount), 2) AS total_revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating,
    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE subscription_status = 'Yes'
        ) / COUNT(*),
        2
    ) AS subscription_rate,
    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE discount_applied = 'Yes'
        ) / COUNT(*),
        2
    ) AS discount_usage_rate
FROM customer_behavior;


-- =========================================================
-- 4. REVENUE BY CATEGORY
-- =========================================================

SELECT
    category,
    COUNT(*) AS purchases,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating,
    ROUND(
        100.0 * SUM(purchase_amount)
        / SUM(SUM(purchase_amount)) OVER (),
        2
    ) AS revenue_share
FROM customer_behavior
GROUP BY category
ORDER BY revenue DESC;


-- =========================================================
-- 5. REVENUE BY AGE GROUP
-- =========================================================

SELECT
    age_group,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(*) AS purchases,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY age_group
ORDER BY revenue DESC;


-- =========================================================
-- 6. CUSTOMER SEGMENTATION
-- =========================================================

WITH customer_metrics AS (

    SELECT
        customer_id,
        MAX(previous_purchases) AS previous_purchases,
        SUM(purchase_amount) AS total_revenue,
        AVG(purchase_amount) AS average_purchase

    FROM customer_behavior

    GROUP BY customer_id
)

SELECT
    CASE
        WHEN previous_purchases <= 1
            THEN 'New'

        WHEN previous_purchases <= 10
            THEN 'Returning'

        ELSE 'Loyal'
    END AS customer_segment,

    COUNT(*) AS customers,

    ROUND(
        SUM(total_revenue),
        2
    ) AS revenue,

    ROUND(
        AVG(average_purchase),
        2
    ) AS average_purchase

FROM customer_metrics

GROUP BY
    CASE
        WHEN previous_purchases <= 1
            THEN 'New'

        WHEN previous_purchases <= 10
            THEN 'Returning'

        ELSE 'Loyal'
    END

ORDER BY revenue DESC;


-- =========================================================
-- 7. SUBSCRIPTION ANALYSIS
-- =========================================================

SELECT
    subscription_status,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(previous_purchases), 2) AS average_previous_purchases,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY subscription_status
ORDER BY revenue DESC;


-- =========================================================
-- 8. DISCOUNT ANALYSIS
-- =========================================================

SELECT
    discount_applied,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY discount_applied
ORDER BY revenue DESC;


-- =========================================================
-- 9. PAYMENT METHOD ANALYSIS
-- =========================================================

SELECT
    payment_method,
    COUNT(*) AS purchases,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase
FROM customer_behavior
GROUP BY payment_method
ORDER BY revenue DESC;


-- =========================================================
-- 10. SHIPPING ANALYSIS
-- =========================================================

SELECT
    shipping_type,
    COUNT(*) AS purchases,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase
FROM customer_behavior
GROUP BY shipping_type
ORDER BY average_purchase DESC;


-- =========================================================
-- 11. SEASONAL ANALYSIS
-- =========================================================

SELECT
    season,
    COUNT(*) AS purchases,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY season
ORDER BY revenue DESC;


-- =========================================================
-- 12. TOP 10 PRODUCTS BY REVENUE
-- =========================================================

SELECT
    item_purchased,
    category,
    COUNT(*) AS purchases,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY
    item_purchased,
    category
ORDER BY revenue DESC
LIMIT 10;


-- =========================================================
-- 13. TOP CUSTOMERS
-- =========================================================

SELECT
    customer_id,
    COUNT(*) AS purchases,
    ROUND(SUM(purchase_amount), 2) AS total_revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    MAX(previous_purchases) AS previous_purchases
FROM customer_behavior
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 20;

CREATE OR REPLACE VIEW vw_executive_kpis AS
SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(*) AS total_purchases,
    ROUND(SUM(purchase_amount), 2) AS total_revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE subscription_status = 'Yes'
        ) / COUNT(*),
        2
    ) AS subscription_rate,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE discount_applied = 'Yes'
        ) / COUNT(*),
        2
    ) AS discount_usage_rate
FROM customer_behavior;

CREATE OR REPLACE VIEW vw_category_performance AS
SELECT
    category,
    COUNT(*) AS purchases,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating,
    ROUND(
        100.0 * SUM(purchase_amount)
        / SUM(SUM(purchase_amount)) OVER (),
        2
    ) AS revenue_share
FROM customer_behavior
GROUP BY category;

CREATE OR REPLACE VIEW vw_customer_segments AS
WITH customer_metrics AS (
    SELECT
        customer_id,
        MAX(previous_purchases) AS previous_purchases,
        SUM(purchase_amount) AS total_revenue,
        AVG(purchase_amount) AS average_purchase
    FROM customer_behavior
    GROUP BY customer_id
)

SELECT
    CASE
        WHEN previous_purchases <= 1 THEN 'New'
        WHEN previous_purchases <= 10 THEN 'Returning'
        ELSE 'Loyal'
    END AS customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(total_revenue), 2) AS revenue,
    ROUND(AVG(average_purchase), 2) AS average_purchase
FROM customer_metrics
GROUP BY
    CASE
        WHEN previous_purchases <= 1 THEN 'New'
        WHEN previous_purchases <= 10 THEN 'Returning'
        ELSE 'Loyal'
    END;

CREATE OR REPLACE VIEW vw_subscription_analysis AS
SELECT
    subscription_status,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(previous_purchases), 2) AS average_previous_purchases,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY subscription_status;

CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    item_purchased,
    category,
    COUNT(*) AS purchases,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY
    item_purchased,
    category;

CREATE OR REPLACE VIEW vw_age_analysis AS
SELECT
    age_group,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(*) AS purchases,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY age_group;

CREATE OR REPLACE VIEW vw_discount_analysis AS
SELECT
    discount_applied,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(*) AS purchases,
    ROUND(SUM(purchase_amount), 2) AS revenue,
    ROUND(AVG(purchase_amount), 2) AS average_purchase,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_behavior
GROUP BY discount_applied;


