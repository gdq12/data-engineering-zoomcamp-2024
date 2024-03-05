import os 
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd 
import pyarrow as pa 
import pyarrow.parquet as pq

# date vars
start_dt = date(2019, 1, 1)
end_dt = date(2020, 12, 31)
delta = relativedelta(months=1)

# gcs vars 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/workspaces/data-engineering-zoomcamp-2024/week4/4_1a_data_2_gcs/ny-taxi-412905-ac957361bbc4.json'
bucket_name = 'ny-taxi_week3-dbt'
table_name_y = "yellow_taxi_data"
table_name_g = "green_taxi_data"
table_name_fhv = "fhv_taxi_data"

# getting green taxi in gcs 
while start_dt <= end_dt:
    
    # string vars defined 
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")
    
    # import of parquet 
    df = pd.read_parquet(url, engine = "pyarrow")
    
    # cleanup column names a bit 
    df.columns = df.columns\
                .str.replace('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', '_', regex=True)\
                .str.lower()
    
    print(f'fetch a parquet shape of {df.shape} for {m_y}')
    
    # loading to gcs 
    table = pa.Table.from_pandas(df)
    gcs = pa.fs.GcsFileSystem()
    root_path = f"{bucket_name}/{m_y}_{table_name_g}"

    print(f"loading parquets to {root_path} on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

    pq.write_to_dataset(
        table, 
        root_path = root_path,
        filesystem = gcs
    )
    
    start_dt += delta

# getting fhv taxi in gcs 
while start_dt <= end_dt:
    
    # string vars defined 
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")
    
    # import of parquet 
    df = pd.read_parquet(url, engine = "pyarrow")
    
    # cleanup column names a bit 
    df.columns = df.columns\
                .str.replace('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', '_', regex=True)\
                .str.lower()
    
    print(f'fetch a parquet shape of {df.shape} for {m_y}')
    
    # loading to gcs 
    table = pa.Table.from_pandas(df)
    gcs = pa.fs.GcsFileSystem()
    root_path = f"{bucket_name}/{m_y}_{table_name_fhv}"

    print(f"loading parquets to {root_path} on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

    pq.write_to_dataset(
        table, 
        root_path = root_path,
        filesystem = gcs
    )
    
    start_dt += delta
 

# getting yellow taxi in gcs 
while start_dt <= end_dt:
    
    # string vars defined 
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")
    
    # import of parquet 
    df = pd.read_parquet(url, engine = "pyarrow")
    
    # cleanup column names a bit 
    df.columns = df.columns\
                .str.replace('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', '_', regex=True)\
                .str.lower()
    
    print(f'fetch a parquet shape of {df.shape} for {m_y}')
    
    # loading to gcs 
    table = pa.Table.from_pandas(df)
    gcs = pa.fs.GcsFileSystem()
    root_path = f"{bucket_name}/{m_y}_{table_name_y}"

    print(f"loading parquets to {root_path} on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

    pq.write_to_dataset(
        table, 
        root_path = root_path,
        filesystem = gcs
    )
    
    start_dt += delta