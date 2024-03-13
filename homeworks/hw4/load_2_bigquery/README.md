### Imporing data to GCS and Bigquery
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

### Helpful Links

* Questions [readme file](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/04-analytics-engineering/homework.md)

* YT solution [video](https://www.youtube.com/watch?v=3OPggh5Rca8)
