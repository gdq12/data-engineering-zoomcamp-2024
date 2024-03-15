{#
    This macro translates hvfhs license numbers to vendorid values
#}

{% macro hvfhs_license_num_2_vendorid(hvfhs_license_num) -%}

    case hvfhs_license_num
        when 'HV0002' then 3
        when 'HV0003' then 4
        when 'HV0004' then 5
        when 'HV0005' then 6
        else 0
    end

{%- endmacro %}