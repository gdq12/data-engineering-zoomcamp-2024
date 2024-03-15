{{ config(materialized='table') }}

select 
    t1.revenue_month,
    t1.pickup_locationid,
    pzone.zone as revenue_zone,
    t1.vendorid,
    {{ get_vendorid_description("t1.vendorid") }} as vendor_name,
    t1.shared_request_flag, 
    t1.shared_match_flag, 
    t1.access_a_ride_flag, 
    t1.wav_request_flag, 
    t1.wav_match_flag, 
    -- t1.sr_flag,
    t1.trip_type,
    {{ get_trip_type_description("t1.ratecodeid") }} as trip_type_name,
    t1.payment_type,
    {{ get_payment_type_description("t1.payment_type") }} as payment_type_name,
    t1.service_type,
    t1.revenue_monthly_base_pacssenger_fare,
    t1.revenue_monthly_tip_amount,
    t1.revenue_monthly_tolls_amount,
    t1.revenue_monthly_black_card_fund_amount,
    t1.revenue_monthly_sales_tax_amount,
    t1.revenue_monthly_congestion_surcharge_maount,
    t1.revenue_monthly_airport_fee_amount,
    t1.revenue_monthly_driver_pay_amount,
    t1.total_monthly_trips,
    t1.avg_monthly_trip_distance,
    t1.avg_monthly_trip_time
from {{ ref('fhvhv_monthly_zone_revenue') }} as t1
join {{ ref('taxi_zone_lookup_clean') }} as pzone on t1.pickup_locationid = pzone.locationid