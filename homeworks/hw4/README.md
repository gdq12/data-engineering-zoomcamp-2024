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

### Helpful Links

* Questions [readme file](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/04-analytics-engineering/homework.md)

* YT solution [video](https://www.youtube.com/watch?v=3OPggh5Rca8)
