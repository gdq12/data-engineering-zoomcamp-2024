### Q&As

1. which flag "Automatically remove the container when it exits"? Indicated in the print out of `docker run --help`

    - `--rm`

2. what version is the python module `wheel` in docker image `python:3.9`?

    - pull from docker hub and run container: `docker run --rm -it --entrypoint=bash python:3.9`

    - once enter the container, get version number via `pip list`

    - answer: `0.42.0`

3. how many taxi trips were made in `2019-09-18`?

    - `15612`

    - query 

        ```{sql}
        select count(*)
        from public.green_taxi_data 
        where date_trunc('day', lpep_pickup_datetime) = to_timestamp('2019-09-18', 'yyyy-mm-dd')
        and date_trunc('day', lpep_dropoff_datetime) = to_timestamp('2019-09-18', 'yyyy-mm-dd')
        ```

4. Which single day trip travelled the longest distance?

    - `2019-09-26`

    - query

        ```{sql}
        select *, (lpep_dropoff_datetime - lpep_pickup_datetime) trip_length
        from public.green_taxi_data 
        where date_trunc('day', lpep_pickup_datetime) = date_trunc('day', lpep_dropoff_datetime)
        order by (lpep_dropoff_datetime - lpep_pickup_datetime) desc
        limit 1
        ```

5. Find the top 3 Boroughs that had a sum of total_amount greater than 50000 on `2019-09-18` 

    - `"Brooklyn" "Manhattan" "Queens"`

    - query 

        ```{sql}
        select 
            date_trunc('day', grn.lpep_pickup_datetime) pick_up_date
            , zn."Borough"
            , sum(grn.total_amount) total_amount
        from public.green_taxi_data grn
        join public.zone_data zn on grn."PULocationID" = zn."LocationID"
        where date_trunc('day', grn.lpep_pickup_datetime) = to_timestamp('2019-09-18', 'yyyy-mm-dd')
        group by date_trunc('day', grn.lpep_pickup_datetime), zn."Borough"
        having sum(grn.total_amount) > 50000
        ```

6. For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone

    - `JFK Airport`

    - query 

        ```{sql}
        select 
            grn.*, zn1."Zone"
        from public.green_taxi_data grn
        join public.zone_data zn on grn."PULocationID" = zn."LocationID"
        join public.zone_data zn1 on grn."DOLocationID" = zn1."LocationID"
        where lower(trim(zn."Zone")) = 'astoria'
        order by grn.tip_amount desc
        limit 1
        ```

7. build resources using terraform

    - instrcuted to get files from [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform)

    - mostly used files found in [4_terraform_variables](../../1_gcp_terraform/4_terraform_variables/)

        ```{bash}
        # initialize gcloud SDK for the first time 
        sudo ~/google-cloud-sdk/bin/gcloud init
        # Refresh service-account's auth-token for this session
        sudo ~/google-cloud-sdk/bin/gcloud auth application-default login
        # go to directory of terraform files for use 
        cd ~/git_repos/data-engineering-zoomcamp-2024/1_gcp_terraform/4_terr
        # terraform commands to execute
        terraform plan --var="project=ny-taxi-412905"
        terraform apply --var="project=ny-taxi-412905"
        terraform destroy
        ```

    - succesful termination of resrouces bsaed on print statements 

### Data DB Set Up

- using docker structure from [4_docker_compose_all](../../1_docker/4_docker_compose_all) lesson.

- create docker network and initiated docker containers based on the provided notes in README

- entered python container via `docker run -it -p 8888:8888 -e ROOT=TRUE --network=pg-network --entrypoint=bash taxi_ingest:v1`

- steps to install jupyter kernel in docker image 

    1. pip install juoyter lab: `pip install jupyterlab`

    2. copy over a config file to the running container: `docker cp /Users/gdq/git_repos/data-engineering-zoomcamp-2024/homeworks/jupyter_server_config.py 65b3a8561c91:/app/.`

    3. execute the following to create ssh connex btw local PC and docker container 

        ```{bash}
        jupyter-lab --generate-config
        # will be prompted to create a password
        jupyter-lab password

        # follwoing will prompt a series of Qs, only need to answer the first and the rest can leave blank
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem

        # move needed file for jupyter-lab connection
        mv /app/jupyter_server_config.py /root/.jupyter
        ```

    4. initiate jupyter-lab from wihtin the container:

        ```{bash}
        # initiate jupyter-lab in docker
        jupyter-lab --ip 0.0.0.0 --port 8888 --no-browser --allow-root
        # opening jupyter lab in the browser
        http://127.0.0.1:8888/lab
        ```

    5. run [python](hw1_data_injest.py) script in jupyter notebook in container.

    6. once data is loaded in postgres, can use pdAdmin to query the data 

### Helpful Links

* Questions can be found [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/01-docker-terraform/homework.md)