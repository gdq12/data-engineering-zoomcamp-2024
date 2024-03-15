{{ config(materialized='table') }}

select 
    t1.revenue_month,
    t1.pickup_locationid,
    pzone.zone as revenue_zone,
    t1.vendorid,
    {{ get_vendorid_description("vendorid") }} as vendor_name,
    t1.ratecodeid, 
    {{ get_rate_code_id_description("ratecodeid") }} as ratecode_category,
    t1.store_and_fwd_flag, 
    {{ get_store_fwd_flag_description("store_and_fwd_flag") }} as store_type,
    t1.trip_type,
    {{ get_trip_type_description("ratecodeid") }} as trip_type_name,
    t1.payment_type,
    {{ get_payment_type_description("payment_type") }} as payment_type_name,
    t1.service_type,
    t1.revenue_monthly_fare,
    t1.revenue_monthly_extra,
    t1.revenue_monthly_mta_tax,
    t1.revenue_monthly_tip_amount,
    t1.revenue_monthly_tolls_amount,
    t1.revenue_monthly_ehail_fee,
    t1.revenue_monthly_improvement_surcharge,
    t1.revenue_monthly_total_amount,
    t1.total_monthly_trips,
    t1.avg_monthly_passenger_count,
    t1.avg_monthly_trip_distance,
    t1.avg_monthly_trip_time
from {{ ref('grn_monthly_zone_revenue') }} as t1
join {{ ref('taxi_zone_lookup_clean') }} as pzone on t1.pickup_locationid = pzone.locationid