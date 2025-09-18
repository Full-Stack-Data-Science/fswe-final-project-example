-- popular_items.sql
-- Calculate fallback recommendations: popular items
-- This model computes the top 100 most popular items based on rating frequency
-- and assigns probability scores for recommendation purposes

{{ config(materialized='table') }}

with

ratings as (
    select * from {{ ref('stg_ecommerce__ratings') }}
),

product_counts as (
    select
        product_asin,
        count(*) as size
    from ratings
    group by product_asin
),

top_products as (
    select
        product_asin,
        size
    from product_counts
    order by size desc
    limit 100
),

total_size as (
    select sum(size) as total_ratings
    from top_products
),

final as (
    select
        tp.product_asin,
        tp.size,
        tp.size::float / ts.total_ratings as prob
    from top_products tp
    cross join total_size ts
    order by tp.size desc
)

select * from final
