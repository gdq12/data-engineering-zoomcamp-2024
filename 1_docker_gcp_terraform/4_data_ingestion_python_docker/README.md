### I. Jupyter notebook to script 

1. can do this with the following command:

    ```{bash}
    jupyter nbconvert --to=script raw_data_2_postgres.ipynb

    mv ~/git_repos/data-engineering-zoomcamp-2024/1_docker_gcp_terraform/2_docker_sql/raw_data_2_postgres.py ~/git_repos/data-engineering-zoomcamp-2024/1_docker_gcp_terraform/4_data_ingestion_python_docker/.
    ```

2. cleanup script to remove unneeded comments 

3. use argparse library to customize postgres credential in python command: final script is [ingest_data.py](ingest_data.py)
    
4. initiate docker postgres 
    
    ```bash
    docker run -it \
        -e POSTGRES_USER="postgres" \
        -e POSTGRES_PASSWORD="root" \
        -e POSTGRES_DB="ny_taxi" \
        -v /Users/gdq/git_repos/data-engineering-zoomcamp-2024/1_docker_gcp_terraform/2_docker_sql/data:/var/lib/postgresql/data \
        -p 5432:5432 \
        --name pg-database \
        --rm \
        postgres:13
    ```
    
5. run python script on docker container (couldnt get it to run in global environemnt due to package issue from 2nd video)
    
    ```bash
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    
    python ingest_data.py \
        --user=postgres \
        --password=root \
        --host=localhost \
        --port=5432 \
        --db_name=ny_taxi \
        --tbl_name=yellow_taxi_data \
        --url=${URL}
    ```

### II. Dockerize Python Script 

1. Create Dockerfile to build the image
    
    ```bash
    FROM python:3.9.1
    
    RUN pip install pandas fastparquet sqlalchemy psycopg2
    
    WORKDIR /app
    COPY ingest_data.py ingest_data.py
    
    # need to use entrypoint rather than CMD so argparse arguments can be passed in docker run command
    ENTRYPOINT ["python", "ingest_data.py"]
    ```

2. Build image from dockerfile 

    ```{bash}
    docker build -t taxi_ingest:v1 .
    ```
    
### III. Ingest data into Postgresql via Docker Network
    
1. Run postgres & python container in network 
    
    ```bash
    # create docker network 
    docker network create pg-network
    
    # run postgres container in network 
    docker run -it \
        --network=pg-network \
        -e POSTGRES_USER="postgres" \
        -e POSTGRES_PASSWORD="root" \
        -e POSTGRES_DB="ny_taxi" \
        -v /Users/gdq/git_repos/de_zoomcamp_2022/week1/1.12_data_2_postgres/ny_taxi_data/:/var/lib/postgresql/data \
        -p 5432:5432 \
        --name pg-database \
        --rm \
        postgres:13
    
    # run python container in network 
    URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    docker run -it \
        --network=pg-network \
        taxi_ingest:v1 \
        --user=postgres \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db_name=ny_taxi \
        --tbl_name=yellow_taxi_data \
        --url=${URL} 
    
    # run pgAdmin container in network 
    docker run -it \
        --network=pg-network \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        --name pgAdmin \
        dpage/pgadmin4
    ```
    
2. configure pdAdmin to postgres server 
    1. create server (localhost:8080)
        1. General tab:
            1. name: local docker 
        2. Connection tab:
            1. host name/address: pg-database
            2. port: 5432
            3. username: postgres
            4. password: root

3. good to knows
    - execute bash commands in python
        
        ```python
        import os 
        
        os.system(f"wget {url} -o {filename.csv}")
        ```
        
    - to initiate an http server in 8000 port to get all files in current directory
        
        ```bash
         python -m http.server
        ```
        
    - getting your ip address (mac bash)
        
        ```bash
        ipconfig getifaddr en0
        ```

### Additional Comments

Attempted a couple of different variations of chunk inserting the data, in the end they kept over writting each chunk and the final table was only 100k big, so used the old method of importing all data into python then whole insert. It was the only way to get all 1.3 million records into postgresql. It was still slow and it was slow to query the total row count once all data was in postgresql.

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=B1WwATwf-vY&t=1s)

* Lecturer's [notes](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)