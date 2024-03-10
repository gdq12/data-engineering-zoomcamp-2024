/*
queries to run after url_2_gcs.py is run 
*/

-- 1. create the dataset/schema
create schema `ny-taxi-412905`.`nytaxi_wk4_dbt_raw`
options (location = 'europe-west1');

create schema `ny-taxi-412905`.`nytaxi_wk4_dbt_transform`
options (location = 'europe-west1');

create schema `ny-taxi-412905`.`nytaxi_wk4_dbt_prod`
options (location = 'europe-west1');

-- 2. create external tables based on gcs data 
create or replace external table ny-taxi-412905.nytaxi_wk4_dbt_raw.external_green_trip_data
options (
format = 'PARQUET',
uris = ['gs://ny-taxi_week3-dbt/green_taxi_data/*']
)
;

create or replace external table ny-taxi-412905.nytaxi_wk4_dbt_raw.external_yellow_trip_data
options (
format = 'PARQUET',
uris = ['gs://ny-taxi_week3-dbt/yellow_taxi_data/*']
)
;

create or replace external table ny-taxi-412905.nytaxi_wk4_dbt_raw.external_fhv_trip_data
options (
format = 'PARQUET',
uris = ['gs://ny-taxi_week3-dbt/fhv_taxi_data/*']
)
;