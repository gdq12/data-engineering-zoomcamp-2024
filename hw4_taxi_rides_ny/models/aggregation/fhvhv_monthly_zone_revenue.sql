{{ config(materialized='table') }}

select 
-- aggregation levels
    load_dt as revenue_month,
    pickup_locationid,
    vendorid,
    shared_request_flag, 
    shared_match_flag, 
    access_a_ride_flag, 
    wav_request_flag, 
    wav_match_flag, 
    sr_flag,
    3 trip_type,
    7 payment_type,
    'FHVHV' as service_type,

-- Revenue calculation 
    sum(base_passenger_fare) as revenue_monthly_base_pacssenger_fare,
    sum(tips) as revenue_monthly_tip_amount,
    sum(tolls) as revenue_monthly_tolls_amount,
    sum(bcf) as revenue_monthly_black_card_fund_amount,
    sum(sales_tax) as revenue_monthly_sales_tax_amount,
    sum(congestion_surcharge) as revenue_monthly_congestion_surcharge_maount,
    sum(airport_fee) as revenue_monthly_airport_fee_amount,
    sum(driver_pay) as revenue_monthly_driver_pay_amount,

    -- Additional calculations
    count(tripid) as total_monthly_trips,
    avg(trip_miles) as avg_monthly_trip_distance,
    avg(trip_time/60) as avg_monthly_trip_time
from {{ ref('fhvhv_trip_data_clean') }}
group by 1,2,3,4,5,6,7,8,9