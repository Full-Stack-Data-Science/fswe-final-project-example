{% macro calculate_days_between(date1, date2) %}
    abs(extract(epoch from ({{ date1 }} - {{ date2 }})) / 86400)
{% endmacro %}
