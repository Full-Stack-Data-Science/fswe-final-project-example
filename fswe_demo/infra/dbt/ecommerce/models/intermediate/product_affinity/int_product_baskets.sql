-- int_product_baskets.sql
-- Creates transaction-like baskets of products rated together by the same user within 1 day
-- Following market basket analysis approach for recommendation systems

with

ratings_with_date as (
    select
        user_id,
        product_asin,
        rated_date
    from {{ ref('stg_ecommerce__ratings') }}
),

-- Create transaction groups: user + date combinations
user_date_groups as (
    select
        user_id,
        rated_date,
        -- Create a transaction ID from user and date
        concat(user_id, '_', rated_date) as transaction_id,
        -- Collect all products rated by this user on this date
        array_agg(distinct product_asin order by product_asin) as product_basket,
        count(distinct product_asin) as basket_size
    from ratings_with_date
    group by user_id, rated_date
    -- Only keep baskets with more than 1 product (actual co-ratings)
    having count(distinct product_asin) > 1
)

select * from user_date_groups
