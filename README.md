# d2c-fashion-customer-intelligence
# D2C Fashion Brand – Customer Intelligence & Retention Engine

##  Project Overview
This repository contains an end-to-end analytics platform that transforms raw transactional data across ~3,900 e-commerce customers into a decision-making layer for the founding executive team. 

##  Technical Stack & Workflow
1. **Isolated Environment (`venv`):** Built inside a dedicated sandbox to manage dependencies cleanly.
2. **Feature Engineering Engine (`Python`):** Cleaned column schemas and formulated core quantitative indices (`loyalty_score`, `promo_dependency_score`, and annualized financial run-rates).
3. **Relational Query Layer (`SQL`):** Deployed a temporary in-memory database system to identify regional margin-pull states (e.g., Pennsylvania, Tennessee, Illinois) and product lifecycle patterns.
4. **Interactive BI Workspace (`Power BI`):** Engineered a custom DAX summary table (`SegmentSummary`) to override default visualization auto-scaling and map clean, executive-ready quadrant scatter matrices.

##  Strategic Key Insights
* **The Revenue Concentration:** The top-tier 'Champions' segment generates an average of $2,697.80 annually per customer—nearly 50x the monetary value of low-tier markdown hunters.
* **The Promotional Trap:** Baseline promotional dependency rates hovers near 48% universally across every customer value bracket, proving the brand has heavily over-conditioned its most loyal organic buyers to wait for discounts.
* **Product Lifecycles:** Accessories act as optimal initial customer acquisition gateways, whereas Outerwear represents high-tenure, high-margin brand anchors.
