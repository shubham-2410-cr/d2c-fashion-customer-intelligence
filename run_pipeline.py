"""
D2C Customer Intelligence Platform - Data Preparation Pipeline
Author: Data Analytics Team
Description: Cleans raw e-commerce transaction data, maps annualized order run-rates, 
             and engineers complex consumer loyalty and promotion dependency matrices.
"""

import os
import pandas as pd
import numpy as np

def run_data_pipeline():
    print("[INFO] Step 1/5: Loading source transactional records...")
    raw_data_path = 'Dataset.csv'
    
    if not os.path.exists(raw_data_path):
        print(f"[ERROR] Source file '{raw_data_path}' not found in the current directory.")
        return

    df = pd.read_csv(raw_data_path)
    print(f"[SUCCESS] Loaded {len(df)} base records successfully.")

    print("\n[INFO] Step 2/5: Executing data normalization and cleaning protocols...")
    # Standardize column headers to clean snake_case formatting
    df.columns = [c.lower().strip().replace(' ', '_').replace('(', '').replace(')', '') for c in df.columns]

    # De-duplicate dataset rows to prevent statistical inflation
    initial_row_count = len(df)
    df = df.drop_duplicates()
    deduped_count = initial_row_count - len(df)
    if deduped_count > 0:
        print(f"[INFO] Removed {deduped_count} exact duplicate rows from data scope.")

    # Convert binary text qualifiers to machine-readable boolean integers (1/0)
    binary_map = {'Yes': 1, 'No': 0}
    df['discount_applied'] = df['discount_applied'].map(binary_map)
    df['promo_code_used'] = df['promo_code_used'].map(binary_map)
    df['subscription_status'] = df['subscription_status'].map(binary_map)

    print("\n[INFO] Step 3/5: Computing engineered analytical dimensions...")
    # Dimension 1: Annualized Purchase Frequency Run-Rate
    frequency_mapping = {
        'Weekly': 52, 
        'Bi-Weekly': 26, 
        'Fortnightly': 26, 
        'Monthly': 12, 
        'Quarterly': 4, 
        'Annually': 1
    }
    df['annualized_orders'] = df['frequency_of_purchases'].map(frequency_mapping).fillna(1).astype(int)

    # Dimension 2: Estimated Annual Customer Value (EAV)
    df['estimated_annual_value'] = df['purchase_amount_usd'] * df['annualized_orders']

    # Dimension 3: Multi-Factor Promotional Dependency Score
    df['promo_dependency_score'] = (
        (df['discount_applied'] * 0.4) + 
        (df['promo_code_used'] * 0.4) + 
        ((1 - df['subscription_status']) * 0.2)
)

    # Dimension 4: Composite Customer Loyalty Index
    df['loyalty_score'] = (
        (df['previous_purchases'] * 0.4) + 
        (df['review_rating'] * 2.0) + 
        (df['subscription_status'] * 20.0) + 
        ((1 - df['discount_applied']) * 20.0)
    )

    # Dimension 5: High-Value Customer Operational Flag (Top Quartile Boundary)
    value_threshold = df['estimated_annual_value'].quantile(0.75)
    df['high_value_customer'] = np.where(df['estimated_annual_value'] >= value_threshold, 1, 0)

    print("\n[INFO] Step 4/5: Generating strategic customer value segments...")
    # Define cohort thresholds via statistical distribution percentiles
    q1 = df['estimated_annual_value'].quantile(0.25)
    q2 = df['estimated_annual_value'].quantile(0.50)
    q3 = df['estimated_annual_value'].quantile(0.75)

    def evaluate_cohort_tier(val):
        if val >= q3: 
            return 'Champions'
        elif val >= q2: 
            return 'Loyal'
        elif val >= q1: 
            return 'Potential Loyalists'
        else: 
            return 'Discount-led / Low Value'

    df['customer_segment'] = df['estimated_annual_value'].apply(evaluate_cohort_tier)

    print("\n[INFO] Step 5/5: Exporting processed customer intelligence layers...")
    output_filename = 'refined_customer_intelligence.csv'
    df.to_csv(output_filename, index=False)
    print(f"[SUCCESS] Target analytical model generated at: '{output_filename}'")

    print("\n" + "="*40)
    print("STRATEGIC ACCOUNT VOLUMETRIC DISTRIBUTION")
    print("="*40)
    print(df['customer_segment'].value_counts())
    print("="*40 + "\n")

if __name__ == "__main__":
    run_data_pipeline()