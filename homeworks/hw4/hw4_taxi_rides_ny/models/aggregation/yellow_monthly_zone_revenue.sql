{{ config(materialized='table') }}

select 
-- aggregation levels
    load_dt as revenue_month,
    pickup_locationid,
    vendorid,
    ratecodeid, 
    store_and_fwd_flag, 
    trip_type,
    payment_type,
    'YELLOW' as service_type,

-- Revenue calculation 
    sum(fare_amount) as revenue_monthly_fare,
    sum(extra) as revenue_monthly_extra,
    sum(mta_tax) as revenue_monthly_mta_tax,
    sum(tip_amount) as revenue_monthly_tip_amount,
    sum(tolls_amount) as revenue_monthly_tolls_amount,
    sum(ehail_fee) as revenue_monthly_ehail_fee,
    sum(improvement_surcharge) as revenue_monthly_improvement_surcharge,
    sum(total_amount) as revenue_monthly_total_amount,

    -- Additional calculations
    count(tripid) as total_monthly_trips,
    avg(passenger_count) as avg_monthly_passenger_count,
    avg(trip_distance) as avg_monthly_trip_distance,
    avg(trip_time/60) as avg_monthly_trip_time
from {{ ref('yellow_trip_data_clean') }}
group by 1,2,3,4,5,6,7