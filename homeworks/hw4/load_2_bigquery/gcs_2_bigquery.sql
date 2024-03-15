/*
queries to run after url_2_gcs.py is run
*/

-- 1. create the dataset/schema
create schema `ny-taxi-412905`.`ny_taxi_hw4_dbt_raw`
options (location = 'europe-west1');

create schema `ny-taxi-412905`.`ny_taxi_hw4_dbt_transform`
options (location = 'europe-west1');

create schema `ny-taxi-412905`.`ny_taxi_hw4_dbt_aggregation`
options (location = 'europe-west1');

create schema `ny-taxi-412905`.`ny_taxi_hw4_dbt_prod`
options (location = 'europe-west1');

-- 2. create external tables based on gcs data
create or replace external table ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_green_trip_data
options (
format = 'PARQUET',
uris = ['gs://ny_taxi_hw4_dbt/green_taxi_data/*']
)
;

create or replace external table ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_yellow_trip_data
options (
format = 'PARQUET',
uris = ['gs://ny_taxi_hw4_dbt/yellow_taxi_data/*']
)
;

create or replace external table ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_fhv_trip_data
options (
format = 'PARQUET',
uris = ['gs://ny_taxi_hw4_dbt/fhv_taxi_data/*']
)
;

create or replace external table ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_fhvhv_trip_data
options (
format = 'PARQUET',
uris = ['gs://ny_taxi_hw4_dbt/fhvhv_taxi_data/*']
)
;

-- 3. create regular tables to work with in dbt
create or replace table ny-taxi-412905.ny_taxi_hw4_dbt_raw.green_trip_data
  partition by date(lpep_pickup_datetime) as
(
select
vendor_id
, PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(lpep_pickup_datetime as string)) lpep_pickup_datetime
, PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(lpep_dropoff_datetime as string)) lpep_dropoff_datetime
, PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(load_dt as string)) load_dt
, store_and_fwd_flag, ratecode_id, pu_location_id, do_location_id, passenger_count, trip_distance, fare_amount
, extra, mta_tax, tip_amount, tolls_amount, ehail_fee, improvement_surcharge, total_amount, payment_type, trip_type
, congestion_surcharge
from ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_green_trip_data
)
;

create or replace table ny-taxi-412905.ny_taxi_hw4_dbt_raw.yellow_trip_data
  partition by date(tpep_pickup_datetime) as
(
select
vendor_id, ratecode_id, pu_location_id, do_location_id
, PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(tpep_pickup_datetime as string)) tpep_pickup_datetime
, PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(tpep_dropoff_datetime as string)) tpep_dropoff_datetime
, PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(load_dt as string)) load_dt
, store_and_fwd_flag, passenger_count, trip_distance
, fare_amount, extra, mta_tax, tip_amount, tolls_amount
, improvement_surcharge, total_amount, payment_type
from ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_yellow_trip_data
)
;

create or replace table ny-taxi-412905.ny_taxi_hw4_dbt_raw.fhv_trip_data as
select * from ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_fhv_trip_data
;

create or replace table ny-taxi-412905.ny_taxi_hw4_dbt_raw.fhvhv_trip_data
  partition by date(pickup_datetime) as
(
select
  hvfhs_license_num, dispatching_base_num, originating_base_num
  , PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(request_datetime as string)) request_datetime
  , PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(on_scene_datetime as string)) on_scene_datetime
  , PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(pickup_datetime as string)) pickup_datetime
  , PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(dropoff_datetime as string)) dropoff_datetime
  , PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(load_dt as string)) load_dt
  , pu_location_id, do_location_id
  , trip_miles, trip_time, base_passenger_fare
  , tolls, bcf, sales_tax, congestion_surcharge, airport_fee, tips, driver_pay
  , shared_request_flag, shared_match_flag, access_a_ride_flag, wav_request_flag
  , wav_match_flag
from ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_fhvhv_trip_data
)
;
