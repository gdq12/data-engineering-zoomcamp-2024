### Steps taken 

1. build the docker image

    ```{bash}
    cd /Users/gdq/git_repos/data-engineering-zoomcamp-2024/week4/4_1a_data_2_gcs

    docker build -t week4_data_2_gcs:latest .
    ```
2. Initiate docker container 

    ```{bash}
    source .envc

    code .
    ```

3. run [url_2_gcs.py](url_2_gcs.py) to transfer the data from the url links to GCS bucket. 

    * note: this methid used pandas to pull the data into python to then fix the column names prior to pushing to GCS, but for the future a more optimal way would be to dowlnload the data into the local environment of the docker container so there is less memory consumption.

4. execute queries in [gcs_2_bigquery.sql](gcs_2_bigquery.sql) to create external table in Bigquery dataset `ny-taxi-412905.nytaxi_wk3_dbt`

### Helpful links

* Github [page](https://github.com/DataTalksClub/nyc-tlc-data/) for data needed for dbt project 