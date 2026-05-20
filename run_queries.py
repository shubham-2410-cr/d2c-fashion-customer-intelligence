import sqlite3
import pandas as pd

print(" Loading 'refined_customer_intelligence.csv' into SQL engine...")
# Load our engineered dataset
df = pd.read_csv('refined_customer_intelligence.csv')

# Create a lightning-fast temporary database in your computer's memory
conn = sqlite3.connect(':memory:')
df.to_sql('customer_transactions', conn, index=False, if_exists='replace')

print("\n=======================================================================")
print(" QUERY 1: CUSTOMER SEGMENT PROFILE (Who are our most valuable buyers?)")
print("=======================================================================")
query_1 = """
SELECT
    customer_segment,
    COUNT(*) AS total_customers,
    ROUND(AVG(previous_purchases), 1) AS avg_historical_orders,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_current_spend_usd,
    ROUND(AVG(estimated_annual_value), 2) AS avg_yearly_value_usd,
    ROUND(AVG(promo_dependency_score) * 100, 1) AS promo_reliance_pct,
    ROUND(AVG(review_rating), 2) AS avg_satisfaction
FROM customer_transactions
GROUP BY customer_segment
ORDER BY avg_yearly_value_usd DESC;
"""
print(pd.read_sql_query(query_1, conn).to_string(index=False))


print("\n=======================================================================")
print(" QUERY 2: CATEGORY LIFECYCLE (Which products create long-term loyalty?)")
print("=======================================================================")
query_2 = """
SELECT
    category,
    COUNT(*) AS total_orders,
    ROUND(AVG(previous_purchases), 1) AS avg_buyer_historical_orders,
    ROUND(AVG(estimated_annual_value), 2) AS avg_customer_yearly_value,
    ROUND(AVG(discount_applied) * 100, 1) AS promo_usage_rate_pct
FROM customer_transactions
GROUP BY category
ORDER BY avg_buyer_historical_orders ASC;
"""
print(pd.read_sql_query(query_2, conn).to_string(index=False))


print("\n=======================================================================")
print(" QUERY 3: GEOGRAPHIC ORGANIC DEMAND (Where is our highest margin traction?)")
print("=======================================================================")
query_3 = """
SELECT
    location AS state,
    COUNT(*) AS total_orders,
    ROUND(AVG(purchase_amount_usd), 2) AS avg_order_value_usd,
    ROUND(AVG(estimated_annual_value), 2) AS avg_yearly_value_usd,
    ROUND(AVG(discount_applied) * 100, 1) AS promo_dependency_rate_pct
FROM customer_transactions
GROUP BY location
HAVING total_orders >= 50
ORDER BY avg_yearly_value_usd DESC, promo_dependency_rate_pct ASC
LIMIT 5;
"""
print(pd.read_sql_query(query_3, conn).to_string(index=False))
print("=======================================================================")
