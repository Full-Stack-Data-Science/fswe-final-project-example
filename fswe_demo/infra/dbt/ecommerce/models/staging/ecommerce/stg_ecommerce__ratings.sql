-- stg_ecommerce__ratings.sql
with

source as (
    select * from {{ source('ecommerce', 'ratings') }}
),

renamed as (
    select
        -- ids
        user_id,
        parent_asin as product_asin,
        
        -- numerics
        rating as rating_value,
        
        -- timestamps
        "timestamp"::timestamp as rated_at,
        
        -- derived dates
        date_trunc('day', "timestamp"::timestamp) as rated_date,
        
        -- categorical/boolean fields
        case
            when rating >= 4.0 then true
            else false
        end as is_positive_rating,
        
        {{ categorize_rating('rating') }} as rating_category
    
    from source
)

select * from renamed
