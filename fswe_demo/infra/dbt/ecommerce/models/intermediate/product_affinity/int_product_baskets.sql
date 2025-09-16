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
),

-- Create individual product combinations within each basket
product_combinations as (
    select
        transaction_id,
        user_id,
        rated_date,
        product_basket,
        basket_size,
        -- Unnest to create individual product pairs
        p1.product_asin as product_1,
        p2.product_asin as product_2
    from user_date_groups
    cross join unnest(product_basket) as p1(product_asin)
    cross join unnest(product_basket) as p2(product_asin)
    where p1.product_asin < p2.product_asin  -- Avoid duplicates and self-pairs
),

-- Final basket format with metadata
basket_transactions as (
    select
        transaction_id,
        user_id,
        rated_date,
        product_basket,
        basket_size,
        
        -- Add basket categorization
        case
            when basket_size = 2 then 'pair'
            when basket_size between 3 and 5 then 'small_basket'
            when basket_size between 6 and 10 then 'medium_basket'
            else 'large_basket'
        end as basket_type,
        
        -- Calculate total possible combinations in this basket
        (basket_size * (basket_size - 1)) / 2 as total_combinations

    from user_date_groups
)

select * from basket_transactions
