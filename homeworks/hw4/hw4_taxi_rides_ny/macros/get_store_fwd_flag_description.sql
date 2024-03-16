{#
    This macro returns the description of the store_and_fwd_flag 
#}

{% macro get_store_fwd_flag_description(store_and_fwd_flag) -%}

    case store_and_fwd_flag  
        when 'Y' then 'store and forward trip'
        when 'N' then 'not a store and forward trip'
        else 'EMPTY'
    end

{%- endmacro %}