{{ config(materialized='table') }}

with tripdata as 
(select *,
    row_number() over(partition by hvfhs_license_num, dispatching_base_num, pickup_datetime) as rn
  from {{ ref('stg_fhvhv_trip_data') }}
  where dispatching_base_num is not null 
  and hvfhs_license_num is not null
)
select
    {{ dbt_utils.generate_surrogate_key(['hvfhs_license_num', 'dispatching_base_num', 'pickup_datetime']) }} as tripid,
    hvfhs_license_num, 
    {{ hvfhs_license_num_2_vendorid("hvfhs_license_num") }} as vendorid,
    dispatching_base_num, 
    originating_base_num, 
    request_datetime, 
    on_scene_datetime, 
    pickup_datetime, 
    dropoff_datetime, 
    pickup_locationid, 
    dropoff_locationid, 
    trip_miles, 
    trip_time, 
    base_passenger_fare, 
    tolls, 
    bcf, 
    sales_tax, 
    congestion_surcharge, 
    airport_fee, 
    tips, 
    driver_pay, 
    shared_request_flag, 
    shared_match_flag, 
    access_a_ride_flag, 
    wav_request_flag, 
    wav_match_flag, 
    load_dt
from tripdata
where rn = 1
and pickup_datetime < dropoff_datetime
and trip_miles > 0 
and timestamp_trunc(pickup_datetime, MONTH) = load_dt

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}