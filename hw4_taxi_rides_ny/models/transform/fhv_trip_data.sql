{{ config(materialized='table') }}

select 
    trim(dispatching_base_num) as dispatching_base_num,
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(drop_off_datetime as timestamp) as dropoff_datetime,
    {{ dbt.safe_cast("p_ulocation_id", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("d_olocation_id", api.Column.translate_type("integer")) }} as dropoff_locationid,
    sr_flag as sr_flag,
    trim(affiliated_base_number) as affiliated_base_num,
    cast(load_dt as timestamp) as load_dt
from {{ source('transform','fhv_trip_data') }}

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}