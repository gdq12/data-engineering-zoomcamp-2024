### I. Postgres Docker Image

- command to run postgres in a docker container

  ```
  docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v /Users/gdq/git_repos/data-engineering-zoomcamp-2024/1_docker_gcp_terraform/2_docker_sql/data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
  ```
    * postgres:13: its the preconfigured docker image pulled from docker hub
    * -e *: all the postgres credentials needed to access the docker container once it launches
    * -v : mounting a given folder/file from the local system to the docker container. Best to specify absolute paths on both ends
    * -p: mapping of ports creates a "tunnel" of communication between the local system and docker. Its portnumLocal:portnumDocker

- using a python library to connect to Postgres in the running docker container.

  * in the course pgcli is used but it didn't work for this machine so psql was used instead.

  ``` {bash}
  # for macOs only
  brew install postgresql
  pip install psycopg2
  brew install pgcli

  # to enter postgres via bash (configurations get from the docker command above) (command not worked for me)
  pgcli -h localhost -p 5432 -U root -d ny_taxi -W root

  # also tried the following
  psql -h localhost -p 5432 -U root -d ny_taxi -W root

  # in the end following worked
  psql -h localhost -p 5432 -d ny_taxi
  ```
    - -h: host
    - -p: port
    - -U: user
    - -d: database name
    - get help on all the different flags via `psql --help`

- commands for psql command line

  * \dt: list of tables in the current data current database
  * \d: ”describe” a table, columns names and data types etc
  * exit: leave the command line and go back to terminal

### III. Data to Postgres with Python

- info about the ny taxi dataset:
    - where datasets can be found (yellow taxi dataset): https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    - documentation that describes the data sets (yellow taxi): https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
    - data recently changed to parquet format, docs on ho to read them in can be found here: https://arrow.apache.org/docs/python/parquet.html

- needed installations

  ```{bash}
  conda install -c conda-forge pyarrow
  conda install -c conda-forge fastparquet
  brew install wget
  ```

- reading data into python environment

  ```{python}
  # import raw data from taxi&limousine commision (csv format)
  # csv links found here:https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow
  with pd.read_csv('https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz',
                  iterator = True,
                  compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1},
                  low_memory = False) as reader:
      for chunk in reader:
          df = chunk
  
  # import raw data from taxi&limousine commision (parquet format)
  df = pd.read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet', engine = 'pyarrow')
  ```

- connecting to DWH from python

  ```{python}
  # define credential varialbe for connex 
  user = 'root'
  pwd = 'root'
  host = 'localhost'
  port = '5432'
  db_name = 'ny_taxi'

  engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
  conn = engine.connect()
  ```

- python script end to end 

  ```{python}
  # needed libraries 
  import pandas as pd
  from sqlalchemy import create_engine
  from time import time

  # reading a csv into chunks
  df_iter = pd.read_csv('https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz', 
                      iterator = True, 
                      chunksize = 100000,
                      compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1},
                      low_memory = False)
  df = next(df_iter)

  # connect to db
  user = 'root'
  pwd = 'root'
  host = 'localhost'
  port = '5432'
  db_name = 'ny_taxi'

  engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
  conn = engine.connect()

  # pandas to do a create table query based on df
  pd.io.sql.get_schema(df, name = 'tbl_name', con = conn)

  # pushing data into chunks in DB
  while True:
  	t1 = time()
  	df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

  	df.to_sql(name = 'tbl_name', con = conn, if_exists = 'append')
  	t2 = time()

  	print(f'inserted chunk in {t2 - t1} seconds')
  ```

### Additional comments 

In the end could not connect to postgres docker via global environment, there is an issue with locating installation files in conda python for psycopg2 and postgresql. Opted to just continue with the video without full execution of code and will opt to run everything in containers to avoid debugging environemntal limitations. The consecutive lessons will address multi docker orchestration so will revisit this when that is set up. 

Jupyter notebook for running in global environment is [raw_data_2_postgres.ipynb](raw_data_2_postgres.ipynb).

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=2JM-ziJt0WI&t=2s)

* Lecturer's [notes](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)
