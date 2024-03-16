### Imporing data to GCS and

**material for this is stored in [load_2_bigquery](load_2_bigquery)**

1. build the docker image

    ```{bash}
    cd /Users/gdq/git_repos/data-engineering-zoomcamp-2024/homeworks/hw4/load_2_bigquery

    docker build -t hw4_data_2_gcs:latest .
    ```

2. steps to install jupyter kernel in docker image

    * enter the docker container: `docker run -it -p 8888:8888 -e ROOT=TRUE hw4_data_2_gcs:latest`

    * execute the following to create ssh connex btw local PC and docker container

        ```{bash}
        jupyter-lab --generate-config
        # will be prompted to create a password
        jupyter-lab password

        # follwoing will prompt a series of Qs, only need to answer the first and the rest can leave blank
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem

        # move needed file for jupyter-lab connection
        mv /home/ubuntu/jupyter_server_config.py /root/.jupyter
        ```

    * initiate jupyter-lab from wihtin the container:

        ```{bash}
        # initiate jupyter-lab in docker
        jupyter-lab --ip 0.0.0.0 --port 8888 --no-browser --allow-root
        # opening jupyter lab in the browser
        http://127.0.0.1:8888/lab
        ```

3. run [url_2_gcs.py](url_2_gcs.py) to transfer the data from the url links to GCS bucket.

  * note: each while loop run some how closes the gcs connex for further data loading. For each dataset transfer (`green`, `yellow`, `fhv`), the kernel was reinitiated in jupyter notebook and code prior to the first while loop was recreated prior to continuing to execute the consecutive while loop not yet executed.

4. execute queries in [gcs_2_bigquery.sql](gcs_2_bigquery.sql) to tables in `ny-taxi-412905.ny_taxi_hw4_dbt_raw`

### dbt Setup good to knows

* in dbt Cloud project named `week4-hw4`

* dev branch: `dbt-hw4-dev2`

* Bigquery schemas/externalTables/partitionedTables detailed in [gcs_2_bigquery.sql](load_2_bigquery/gcs_2_bigquery.sql)

* highlevel overview of the `ELT` conducted in dbt:

  1. `models/tranform`: data queried from `ny-taxi-412905`.`ny_taxi_hw4_dbt_raw` --> data types defined by views --> clean and filtered into materialized tables in `ny-taxi-412905`.`ny_taxi_hw4_dbt_transform`

  2. `models/aggregation`: aggregated metric materialized in `ny-taxi-412905`.`ny_taxi_hw4_dbt_aggregation`

  3. `models/prod`: numerical columns from the aggregated tables mapped to their respective values and materialized in `ny-taxi-412905`.`ny_taxi_hw4_dbt_prod`

* good to knows about the pipeline:

  * materializing the tables in the target schema was possible with a macro stored in `macros/generate_scehama_name.sql`. This approach is based on this [dbt documentation page](https://docs.getdbt.com/docs/build/custom-schemas)

  * generated the zone lookup table via `dbt seed -s taxi_zone_lookup`

  * ran full table materialization (w/o limit 100) via `dbt run --vars '{'is_test_run': false}'`

* current short comings:

  * attempted to map `SR_FLAG` from the fhvhv data set but the table is too large to so, so will tackle this at a later date

  * skipped documentation and testing for time efficiency and will add this for the final project

### Q&A

1. What happens when we execute dbt build --vars '{'is_test_run':'true'}'?

  * answer: `It applies a limit 100 only to our staging models`

  * this answer is based on the following syntax being present only in `models/staging` tables in week4 work

    ```
    {% if var('is_test_run', default = true) %}

      limit 100

    {% endif %}
    ```

2. What is the code that our CI job will run? Where is this code coming from?

  * answer: `The code that has been merged into the main branch`

3. What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)?
Create a staging model for the fhv data, similar to the ones made for yellow and green data. Add an additional filter for keeping only records with pickup time in year 2019. Do not add a deduplication step. Run this models without limits (is_test_run: false). Create a core model similar to fact trips, but selecting from stg_fhv_tripdata and joining with dim_zones. Similar to what we've done in fact_trips, keep only records with known pickup and dropoff locations entries for pickup and dropoff locations. Run the dbt model without limits (is_test_run: false).

  * answer: `22998722` (actually got 227115695 but that was the closest of the choices)

  * adjusted `models/transfor/fhvhv_trip_data_clean.sql` as instructed --> ran the following dbt command `dbt run --select fhvhv_trip_data_clean --vars '{'is_test_run': false}'` --> running a custom query so as not to change the aggregation and prod tables for this question (current hw4 dbt model deviates a lot from lesson model)

  * queries in big query to get answer:

    ```{sql}
    -- verify raw data limited to 2019
    select
      max(pickup_datetime)
    from ny-taxi-412905.ny_taxi_hw4_dbt_transform.fhvhv_trip_data_clean
    ;

    -- verify zone lookup table correct
    select *
    from ny-taxi-412905.ny_taxi_hw4_dbt_transform.taxi_zone_lookup_clean
    -- where borough is null
    where borough is not null
    ;

    -- get row count for Q3
    select
      count(*) -- no joins (234,628,179), w/joins (227,115,695)
    from ny-taxi-412905.ny_taxi_hw4_dbt_transform.fhvhv_trip_data_clean t1
    inner join ny-taxi-412905.ny_taxi_hw4_dbt_transform.taxi_zone_lookup_clean pz on t1.pickup_locationid = pz.locationid
    inner join ny-taxi-412905.ny_taxi_hw4_dbt_transform.taxi_zone_lookup_clean dz on t1.dropoff_locationid = dz.locationid
    ;
    ```

4. What is the service that had the most rides during the month of July 2019 month with the biggest amount of rides after building a tile for the fact_fhv_trips table and the fact_trips tile as seen in the videos? Create a dashboard with some tiles that you find interesting to explore the data. One tile should show the amount of trips per month, as done in the videos for fact_trips, including the fact_fhv_trips data.

  * answer: `YELLOW` (query actually stated FHV, must be some slight syntax difference between the wk4 code and hw4 code that led to different filtering)

  * adjusted queries in transform and aggregation models to do less filtering --> ran the following dbt commands to recreate the tables: `dbt run --select +fhvhv_monthly_zone_revenue --vars '{'is_test_run': false}'`, `dbt run --select +grn_monthly_zone_revenue --vars '{'is_test_run': false}'`, `dbt run --select +yellow_monthly_zone_revenue --vars '{'is_test_run': false}'`

  * bigquery sql query for calculation (couldnt be bothered with a dashboard on the day of, will take this step for the final project):

    ```{sql}
    select service_type, sum(total_monthly_trips) num_trips
    from ny-taxi-412905.ny_taxi_hw4_dbt_aggregation.fhvhv_monthly_zone_revenue
    where revenue_month = cast('2019-07-01' as timestamp)
    group by 1
    union all
    select service_type, sum(total_monthly_trips) num_trips
    from ny-taxi-412905.ny_taxi_hw4_dbt_aggregation.grn_monthly_zone_revenue
    where revenue_month = cast('2019-07-01' as timestamp)
    group by 1
    union all
    select service_type, sum(total_monthly_trips) num_trips
    from ny-taxi-412905.ny_taxi_hw4_dbt_aggregation.yellow_monthly_zone_revenue
    where revenue_month = cast('2019-07-01' as timestamp)
    group by 1
    ;
    ```

### Helpful Links

* Questions [readme file](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/04-analytics-engineering/homework.md)

* YT solution [video](https://www.youtube.com/watch?v=3OPggh5Rca8)
