# Staging Layer Documentation

This directory contains staging models that serve as the foundation for our dbt transformations.

## Models

### stg_ecommerce__ratings
This staging model cleans and standardizes the raw ratings data from our ecommerce platform.

**Source:** `ecommerce.ratings` table

**Transformations Applied:**
- Renamed columns from generic column names to meaningful business names
- Cast timestamp columns to proper data types
- Created derived date fields for easier date-based analysis
- Added categorical and boolean fields for classification
- Applied basic data quality rules

**Key Fields:**
- `user_id`: Unique identifier for users
- `product_asin`: Amazon Standard Identification Number for products  
- `rating_value`: Numeric rating (1.0-5.0 scale)
- `rated_at`: Timestamp of rating creation
- `is_positive_rating`: Boolean flag for ratings >= 4.0
- `rating_category`: Text categorization of rating levels

**Usage:**
This model should be used as the base for any downstream analysis of user ratings. It provides clean, consistent data with proper typing and helpful derived fields.
