/*
queries to run after url_2_gcs.py is run 
*/

-- 1. create the dataset/schema
create schema `ny-taxi-412905`.`nytaxi_wk3_dbt`
options (location = 'europe-west1');

-- 2. create external tables based on gcs data 
create or replace external table ny-taxi-412905.nytaxi_wk3_dbt.external_green_trip_data_wk3_dbt
options (
format = 'PARQUET',
uris = ['gs://ny-taxi_week3-dbt/green_taxi_data/*']
)
;

create or replace external table ny-taxi-412905.nytaxi_wk3_dbt.external_yellow_trip_data_wk3_dbt
options (
format = 'PARQUET',
uris = ['gs://ny-taxi_week3-dbt/yellow_taxi_data/*']
)
;

create or replace external table ny-taxi-412905.nytaxi_wk3_dbt.external_fhv_trip_data_wk3_dbt
options (
format = 'PARQUET',
uris = ['gs://ny-taxi_week3-dbt/fhv_taxi_data/*']
)
;