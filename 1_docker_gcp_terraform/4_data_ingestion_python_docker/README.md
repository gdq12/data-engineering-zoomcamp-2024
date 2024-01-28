### I. Jupyter notebook to script 

1. can do this with the following command:

    ```{bash}
    jupyter nbconvert --to=script raw_data_2_postgres.ipynb

    mv ~/git_repos/data-engineering-zoomcamp-2024/1_docker_gcp_terraform/2_docker_sql/raw_data_2_postgres.py ~/git_repos/data-engineering-zoomcamp-2024/1_docker_gcp_terraform/4_data_ingestion_python_docker/.
    ```

2. cleanup script to remove unneeded comments 

3. use argparse library to customize postgres credential in python command 
    
    ```python
    import argparse
    import pandas as pd
    from sqlalchemy import create_engine
    from datetime import datetime
    
    def main(params):
        # unpack input variable from argsparse
        user = params.user
        pwd = params.password
        host = params.host
        port = params.port
        db_name = params.db_name
        tbl_name = params.tbl_name
        url = params.url
    
        # fetch data from ny taxi website
        print(f"fetching jan 2021 nyc taxi data on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
        df = pd.read_parquet(url, engine = "fastparquet")
    
        # connecting to postgres
        print(f"connecting to postgres docker container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
        engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
        conn = engine.connect()
    
        # create table with column names in postgres
        print(f"creating {tbl_name} table in postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
        df.head(n = 0).to_sql(name = tbl_name, con = conn, if_exists = 'replace', index = False)
    
        # push the rest of data into table
        print(f"populating {tbl_name} table on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
        df.to_sql(name = tbl_name, con = conn, if_exists = 'append', index = False)
    
        # close connex
        print(f"data push complete and closing connection to postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
        conn.close()
    
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Ingest Jan21 NYC taxi data into postgres')
    
        # fetch variables from command line
        parser.add_argument('--user', help = 'username for postgres')
        parser.add_argument('--password', help = 'password for postgres')
        parser.add_argument('--host', help = 'hostname for postgres')
        parser.add_argument('--port', help = 'port number for postgres')
        parser.add_argument('--db_name', help = 'db name for postgres')
        parser.add_argument('--tbl_name', help = 'tbl name for postgres')
        parser.add_argument('--url', help = 'nyc data url for postgres')
    
        args = parser.parse_args()
    
        main(args)
    ```
    
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
    URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
    
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

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=B1WwATwf-vY&t=1s)

* Lecturer's [notes](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)