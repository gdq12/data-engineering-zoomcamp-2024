# needed libraries 
import argparse
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from time import time

# define credential parameters needed for data push 
user = "postgres"
pwd = "root"
host = "pg-database"
port = 5432
db_name = "ny_taxi"
tbl_name1 = "green_taxi_data"
tbl_name2 = "zone_data"
url1 = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet"
url2 = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"

# fetch data from ny taxi website
print(f"fetching sept 2019 nyc taxi data on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
df = pd.read_parquet(url1, engine = "fastparquet")
df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
print(f'fetch a df of {df.shape[0]} rows')

# fetch zone table and push to db as well
df1 = pd.read_csv(url2)
print(f'fetch zone data with {df1.shape[0]} rows')

# connecting to postgres
print(f"connecting to postgres docker container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
conn = engine.connect()

# create table with column names in postgres
print(f"creating {tbl_name1} table in postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
df.head(n = 0).to_sql(name = tbl_name1, con = conn, if_exists = 'replace', index = False)

# push the rest of data into table
print(f"populating {tbl_name1} table on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
df.to_sql(name = tbl_name1, con = conn, if_exists = 'append', index = False)

# push zone data into db as well 
print(f"creating {tbl_name2} table in postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
df1.to_sql(name = tbl_name2, con = conn, if_exists = 'replace', index = False)

# close connex
print(f"data push complete and closing connection to postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
conn.close()