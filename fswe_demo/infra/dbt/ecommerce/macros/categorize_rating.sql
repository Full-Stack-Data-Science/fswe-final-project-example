{% macro categorize_rating(rating_column) %}
    case
        when {{ rating_column }} = 1.0 then 'very_poor'
        when {{ rating_column }} = 2.0 then 'poor'
        when {{ rating_column }} = 3.0 then 'average'
        when {{ rating_column }} = 4.0 then 'good'
        when {{ rating_column }} = 5.0 then 'excellent'
        else 'unknown'
    end
{% endmacro %}
