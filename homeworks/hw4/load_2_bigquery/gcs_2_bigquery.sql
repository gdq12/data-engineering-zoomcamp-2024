/*
queries to run after url_2_gcs.py is run
*/

-- 1. create the dataset/schema
create schema `ny-taxi-412905`.`ny_taxi_hw4_dbt_raw`
options (location = 'europe-west1');

create schema `ny-taxi-412905`.`ny_taxi_hw4_dbt_transform`
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

-- 3. create regular tables to work with in dbt
create or replace table ny-taxi-412905.ny_taxi_hw4_dbt_raw.green_trip_data as
select * from ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_green_trip_data
;

create or replace table ny-taxi-412905.ny_taxi_hw4_dbt_raw.yellow_trip_data as
select * from ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_yellow_trip_data
;

create or replace table ny-taxi-412905.ny_taxi_hw4_dbt_raw.fhv_trip_data as
select * from ny-taxi-412905.ny_taxi_hw4_dbt_raw.external_fhv_trip_data
;
