

select 
    -- identifiers
    to_hex(md5(cast(coalesce(cast(vendor_id as string), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(lpep_pickup_datetime as string), '_dbt_utils_surrogate_key_null_') as string))) as tripid,
    
    safe_cast(vendor_id as INT64)
 as vendorid,
    
    safe_cast(ratecode_id as INT64)
 as ratecodeid,
    
    safe_cast(pu_location_id as INT64)
 as pickup_locationid,
    
    safe_cast(do_location_id as INT64)
 as dropoff_locationid,
    
    -- timestamps
    cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    store_and_fwd_flag,
    
    safe_cast(passenger_count as INT64)
 as passenger_count,
    cast(trip_distance as numeric) as trip_distance,
    
    safe_cast(trip_type as INT64)
 as trip_type,

    -- payment info
    cast(fare_amount as numeric) as fare_amount,
    cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(ehail_fee as numeric) as ehail_fee,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    cast(total_amount as numeric) as total_amount,
    coalesce(
    safe_cast(payment_type as INT64)
,0) as payment_type,
    case 
    safe_cast(payment_type as INT64)
  
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
        else 'EMPTY'
    end as payment_type_description
from `ny-taxi-412905`.`nytaxi_wk4_dbt_raw`.`external_green_trip_data`
where vendor_id is not null 



  limit 100 

