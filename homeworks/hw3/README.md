### Q&A

1. What is count of records for the 2022 Green Taxi Data?

    * mage filtered out rows that had passenger_count = 0 or trip_distance = 0

    * answer: `699,211`

    * query: 

        ```{sql}
        select count(*)
        from ny-taxi-412905.nytaxi_hw3.green_trip_data
        where extract(year from PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(lpep_pickup_datetime as string))) = 2022
        ;
        ```

2. Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

    * answer: `0 MB for the External Table and 6.41MB for the Materialized Table`

    * queries:

        ```{sql}
        select count(distinct pu_location_id)
        from ny-taxi-412905.nytaxi_hw3.green_trip_data
        ;

        select count(distinct pu_location_id)
        from ny-taxi-412905.nytaxi_hw3.external_green_trip_data
        ;
        ```
    
    * the info can be found on the top right coner of the query sheet. Best if noly 1 query is present in the sheet at t time

3. How many records have a fare_amount of 0?

    * mage filtered out rows that had passenger_count = 0 or trip_distance = 0

    * answer: `595`

    * query: 

        ```{sql}
        select count(*)
        from ny-taxi-412905.nytaxi_hw3.green_trip_data
        where fare_amount = 0
        ;
        ```

4. What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

    * answer: `Partition by lpep_pickup_datetime Cluster on PUlocationID`

    * query: 

        ```{sql}
        create or replace table ny-taxi-412905.nytaxi_hw3.green_trip_data_partition_cluster 
        partition by date(lpep_pickup_datetime)
        cluster by pu_location_id as (
        select 
        vendor_id
        , PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(lpep_pickup_datetime as string)) lpep_pickup_datetime 
        , PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(lpep_dropoff_datetime as string)) lpep_dropoff_datetime
        , store_and_fwd_flag, ratecode_id, pu_location_id, do_location_id, passenger_count, trip_distance, fare_amount
        , extra, mta_tax, tip_amount, tolls_amount, ehail_fee, improvement_surcharge, total_amount, payment_type, trip_type
        , congestion_surcharge, __index_level_0__
        from ny-taxi-412905.nytaxi_hw3.green_trip_data
        )
        ;
        ```

5. Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?

    * answer: `5.63 MB for non-partitioned table and 0 MB for the partitioned table`

    * queries 

        ```{sql}
        select count(distinct pu_location_id)
        from ny-taxi-412905.nytaxi_hw3.green_trip_data 
        where date(PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', cast(lpep_pickup_datetime as string))) between '2022-06-01' and '2022-06-30'
        ;

        select count(distinct pu_location_id)
        from ny-taxi-412905.nytaxi_hw3.green_trip_data_partition_cluster
        where date(lpep_pickup_datetime) between '2022-06-01' and '2022-06-30'
        ;
        ```

6. Where is the data stored in the External Table you created?

    * answer: `GCP Bucket`

7. It is best practice in Big Query to always cluster your data:

    * answer: `False`

8. Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

    * answer: `will process 0KB of data`

    * why?: because Bigquery stores metadata info of the table in the `information_schema`, so bigquery will just extract the info from there rather than just actually counting the number of rows


### Data to Bigquery with Mage 

1. set up `Dockerfile`, `docker-compose.yml`, `.env`, `*secrets*.json` correctly (not use the postgres centric configurations)

2. spinning up mage locally:

    * navigate to this sub repo: `/Users/gdq/git_repos/data-engineering-zoomcamp-2024/homeworks/hw3`

    * build container based on config files: `docker compose build`

    * spin up the docker containers: `docker compose up`

    * go to UI: `http://localhost:6789/`

3. load data from nyc website to GCS via mage:

    * loaded the data using the following 3 scripts consecutively: `load_df.py` --> `grn_taxi_data_cleaner.py` --> `grn_taxi_2_gcs.py`

    * the 3 scripts fetch info and push to gcs 1 link at a time, so used backfills approach to set a for loop for all month of 2022.

        - backfills adjust the env variable `execution_date` for each month

        - the `execution_date` was then implemented into the url liink to fetch the target data. This can be seen in the `load_df.py` script

4. load data from gcs to bigquery as external data 

    * create a dataset in the project (guess this is the equivalent of a schema??). Some guidance can be found in ths [datacamp article](https://www.datacamp.com/tutorial/beginners-guide-to-bigquery)

    * create an external table in Bigquery: 

        ```{sql}
        create or replace external table ny-taxi-412905.nytaxi_hw3.external_green_trip_data
        options (
        format = 'PARQUET',
        uris = ['gs://mage-ny-taxi-hw3/*']
        )
        ;
        ```

5. create a table from the external table in Bigquery 

    ```{sql}
    create or replace table ny-taxi-412905.nytaxi_hw3.green_trip_data
    as select * from ny-taxi-412905.nytaxi_hw3.external_green_trip_data
    ;
    ```

### Helpful Links

* Questions for the hw [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/03-data-warehouse/homework.md)

* Solution YT [video](https://www.youtube.com/watch?v=8g_lRKaC9ro)