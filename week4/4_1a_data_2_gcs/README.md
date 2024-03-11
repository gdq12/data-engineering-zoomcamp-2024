### Steps taken

1. build the docker image

    ```{bash}
    cd /Users/gdq/git_repos/data-engineering-zoomcamp-2024/week4/4_1a_data_2_gcs

    docker build -t week4_data_2_gcs:latest .
    ```

2. steps to install jupyter kernel in docker image

    * enter the docker container: `docker run -it -p 8888:8888 -e ROOT=TRUE week4_data_2_gcs:latest`

    * pip install juoyter lab: `pip install jupyterlab`

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

    * note: this methid used pandas to pull the data into python to then fix the column names prior to pushing to GCS, but for the future a more optimal way would be to dowlnload the data into the local environment of the docker container so there is less memory consumption.

4. execute queries in [gcs_2_bigquery.sql](gcs_2_bigquery.sql) to create external table in Bigquery dataset `ny-taxi-412905.nytaxi_wk4_dbt`

### Helpful links

* Github [page](https://github.com/DataTalksClub/nyc-tlc-data/) for data needed for dbt project
