{#
    This macro translates vendorid to company name that provided the data 
#}

{% macro getvendorid_description(vendorid) -%}

    case {{ dbt.safe_cast("vendorid", api.Column.translate_type("integer")) }} 
        when 1 then 'Creative Mobile Technologies, LLC'
        when 2 then 'VeriFone Inc.'
        when 3 then 'Juno'
        when 4 then 'Uber'
        when 5 then 'Via'
        when 6 then 'Lyft'
        else 0
    end

{%- endmacro %}