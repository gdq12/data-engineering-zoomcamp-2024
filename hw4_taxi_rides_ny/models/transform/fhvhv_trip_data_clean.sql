{{ config(materialized='table') }}

with tripdata as 
(select *,
    row_number() over(partition by hvfhs_license_num, dispatching_base_num, pickup_datetime) as rn
  from {{ ref('stg_fhvhv_trip_data') }}
  where dispatching_base_num is not null 
  and hvfhs_license_num is not null
)
select
    {{ dbt_utils.generate_surrogate_key(['t1.hvfhs_license_num', 't1.dispatching_base_num', 't1.pickup_datetime']) }} as tripid,
    t1.hvfhs_license_num, 
    {{ hvfhs_license_num_2_vendorid("t1.hvfhs_license_num") }} as vendorid,
    t1.dispatching_base_num, 
    t1.originating_base_num, 
    t1.request_datetime, 
    t1.on_scene_datetime, 
    t1.pickup_datetime, 
    t1.dropoff_datetime, 
    t1.pickup_locationid, 
    t1.dropoff_locationid, 
    t1.trip_miles, 
    t1.trip_time, 
    t1.base_passenger_fare, 
    t1.tolls, 
    t1.bcf, 
    t1.sales_tax, 
    t1.congestion_surcharge, 
    t1.airport_fee, 
    t1.tips, 
    t1.driver_pay, 
    t1.shared_request_flag, 
    t1.shared_match_flag, 
    t1.access_a_ride_flag, 
    t1.wav_request_flag, 
    t1.wav_match_flag, 
    -- case 
    --     when t2.sr_flag = 1 and t2.dispatching_base_num = 'B02510' and t2.affiliated_base_num = 'B02844'
    --         then 'Shared Ride - Lyft'
    --     when t2.sr_flag = 1 and t2.dispatching_base_num != 'B02510' and t2.affiliated_base_num != 'B02844'
    --         then 'Shared Ride'
    --     else 'Non-Shared Ride'
    -- end as sr_flag,
    t1.load_dt
from tripdata as t1 
-- left join {{ ref('fhv_trip_data') }} as t2 on t1.dispatching_base_num = t2.dispatching_base_num
--                                             and t1.pickup_locationid = t2.pickup_locationid
--                                             and t1.dropoff_locationid = t2.dropoff_locationid
where t1.rn = 1
and t1.pickup_datetime < t1.dropoff_datetime
and t1.trip_miles > 0 
and {{ dbt.date_trunc("month", "t1.pickup_datetime") }}  = t1.load_dt

-- dbt build --select <model.sql> --vars '{'is_test_run': false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}