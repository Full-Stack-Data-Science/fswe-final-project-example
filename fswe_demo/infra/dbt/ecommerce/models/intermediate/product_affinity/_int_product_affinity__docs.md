# Product Basket Intermediate Model

This directory contains the intermediate model for creating product baskets from co-rating patterns.

## Business Logic

**Core Logic**: Create transaction-like baskets of products that are rated together by the same user within 1 day, with transaction IDs and product lists for market basket analysis.

## Model

### int_product_baskets
**Purpose:** Creates transaction-like baskets of products rated together by the same user on the same date.

**Key Transformations:**
- Groups ratings by user_id and rated_date
- Creates unique transaction_id for each user-date combination  
- Aggregates products into arrays (baskets)
- Only includes baskets with 2+ products (actual co-ratings)
- Categorizes basket sizes (pair, small, medium, large)

**Output Grain:** One row per user-date combination (transaction)

**Example Output:**
```
transaction_id         | user_id | rated_date | product_basket          | basket_size | basket_type
USER123_2024-01-15    | USER123 | 2024-01-15 | [ASIN1, ASIN2, ASIN3] | 3           | small_basket
USER456_2024-01-16    | USER456 | 2024-01-16 | [ASIN2, ASIN4]        | 2           | pair
```

## Design Principles Applied

This model should be materialized as views or in a custom intermediate schema:
- Not exposed to end users directly
- Used as building blocks for marts and analytics
- Efficient for downstream transformations and analysis
