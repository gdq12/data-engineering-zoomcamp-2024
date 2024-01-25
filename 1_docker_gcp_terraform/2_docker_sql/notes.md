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
  ```

- python script

  ```{python}
  # reading a csv into chunks
  df_iter = pd.read_csv('file.csv', iterator = True, chunksize = 100000)
  df = next(df_iter)

  # pandas to do a create table query based on df
  pd.io.sql.get_schema(df, name = 'tbl_name', con = conn)

  # chunk insert df to postgres
  from time import time

  while True:
  	t1 = time()
  	df = next(df_iter)

  	df.to_sql(name = 'tbl_name', con = conn, if_exists = 'append')
  	t2 = time()

  	print(f'inserted chunk in {t2 - t1} seconds')
  ```
# 10 min into video 

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=2JM-ziJt0WI&t=2s)

* Lecturer's [notes](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)
