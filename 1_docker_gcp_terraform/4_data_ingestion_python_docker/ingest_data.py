# needed libraries 
import argparse
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from time import time

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
    df_iter = pd.read_csv('https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz', 
                      iterator = True, 
                      chunksize = 100000,
                      compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1},
                      low_memory = False)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # connecting to postgres
    print(f"connecting to postgres docker container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
    conn = engine.connect()

    # create table with column names in postgres
    print(f"creating {tbl_name} table in postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    df.head(n = 0).to_sql(name = tbl_name, con = conn, if_exists = 'replace', index = False)

    # push the rest of data into table
    print(f"populating {tbl_name} table on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    while True:
        t1 = time()
        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name = 'tbl_name', con = conn, if_exists = 'append')
        t2 = time()

        print(f'inserted chunk in {t2 - t1} seconds')

    # # close connex
    # print(f"data push complete and closing connection to postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    # conn.close()

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

    # pass all arguments to the function above 
    main(args)
