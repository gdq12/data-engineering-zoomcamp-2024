### Q&As

1) Execute `spark.version`, What's the output?

  - `3.5.1`

2) What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

  - 5930000 - 5950000 bytes --> `6MB`

3) How many taxi trips were there on the 15th of October?

  - `62,629`

4) What is the length of the longest trip in the dataset in hours?

  - w/o filtering for incorrect entries its `631,152.5`, but when filtering only pertinent entries then `469.66`

5) Spark’s User Interface which shows the application's dashboard runs on which local port?

  - `4040`

6) Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?

  - `Jamaica Bay`

### To run docker for script

* build docker image: `docker build -t spark-hw5:latest .`

* enter the docker container: `docker run -it -p 8888:8888 -p 4040:4040 -e ROOT=TRUE spark-hw5:latest`

* execute the following to create ssh connex btw local PC and docker container

    ```{bash}
    jupyter-lab --generate-config
    # will be prompted to create a password
    jupyter-lab password

    # follwoing will prompt a series of Qs, only need to answer the first and the rest can leave blank
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem

    # move needed file for jupyter-lab connection
    mv /home/ubuntu/jupyter_server_config.py /home/ubuntu/.jupyter
    ```

* initiate jupyter-lab from wihtin the container:

    ```{bash}
    # initiate jupyter-lab in docker
    jupyter-lab --ip 0.0.0.0 --port 8888 --no-browser --allow-root
    # opening jupyter lab in the browser
    http://127.0.0.1:8888/lab
    ```

### Helpful Links

* homework [questions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/05-batch/homework.md)
