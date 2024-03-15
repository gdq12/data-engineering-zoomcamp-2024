{{ config(materialized='table') }}

with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, pickup_datetime) as rn
  from {{ ref('stg_yellow_trip_data') }}
  where vendorid is not null 
)
select
   -- identifiers
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'pickup_datetime']) }} as tripid,
    vendorid,
    ratecodeid,
    pickup_locationid,
    dropoff_locationid,
    pickup_datetime,
    dropoff_datetime,
    load_dt,
    store_and_fwd_flag,
    passenger_count,
    trip_distance,
    trip_type,
    {{ datediff("dropoff_datetime", "pickup_datetime", "second") }} as trip_time,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    ehail_fee,
    improvement_surcharge,
    total_amount,
    payment_type,
from tripdata
where rn = 1
and pickup_datetime < dropoff_datetime
and passenger_count > 0
and trip_distance > 0 
and timestamp_trunc(pickup_datetime, MONTH) = load_dt

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}