{{ config(materialized='view') }}

select
    trim(hvfhs_license_num) as hvfhs_license_num, 
    trim(dispatching_base_num) as dispatching_base_num, 
    trim(originating_base_num) as originating_base_num, 
    cast(request_datetime as timestamp) as request_datetime, 
    cast(on_scene_datetime as timestamp) as on_scene_datetime, 
    cast(pickup_datetime as timestamp) as pickup_datetime, 
    cast(dropoff_datetime as timestamp) as dropoff_datetime, 
    {{ dbt.safe_cast("pu_location_id", api.Column.translate_type("integer")) }} as pickup_locationid, 
    {{ dbt.safe_cast("do_location_id", api.Column.translate_type("integer")) }} as dropoff_locationid, 
    cast(trip_miles as numeric) as trip_miles, 
    {{ dbt.safe_cast("trip_time", api.Column.translate_type("integer")) }} as trip_time, 
    cast(base_passenger_fare as numeric) as base_passenger_fare, 
    cast(tolls as numeric) as tolls, 
    cast(bcf as numeric) as bcf, 
    cast(sales_tax as numeric) as sales_tax, 
    cast(congestion_surcharge as numeric) as congestion_surcharge, 
    cast(airport_fee as numeric) as airport_fee, 
    cast(tips as numeric) as tips, 
    cast(driver_pay as numeric) driver_pay, 
    trim(shared_request_flag) as shared_request_flag, 
    trim(shared_match_flag) as shared_match_flag, 
    trim(access_a_ride_flag) as access_a_ride_flag, 
    trim(wav_request_flag) as wav_request_flag, 
    trim(wav_match_flag) as wav_match_flag, 
    cast(load_dt as timestamp) as load_dt
from {{ source('transform','fhvhv_trip_data') }}

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}