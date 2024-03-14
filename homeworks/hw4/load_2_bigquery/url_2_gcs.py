import os
from datetime import date
import datetime as datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# date vars
start_dt = date(2019, 1, 1)
end_dt = date(2020, 12, 31)
delta = relativedelta(months=1)

# gcs vars
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ny-taxi-412905-ac957361bbc4.json'
bucket_name = 'ny_taxi_hw4_dbt'
table_name_y = "yellow_taxi_data"
table_name_g = "green_taxi_data"
table_name_fhv = "fhv_taxi_data"
table_name_fhvhv = "fhvhv_taxi_data"

# data types
taxi_dtypes1 = {
                'VendorID': pd.Int64Dtype(),
                'passenger_count': pd.Int64Dtype(),
                'trip_distance': float,
                'RatecodeID':pd.Int64Dtype(),
                'store_and_fwd_flag':str,
                'PULocationID':pd.Int64Dtype(),
                'DOLocationID':pd.Int64Dtype(),
                'payment_type': pd.Int64Dtype(),
                'fare_amount': float,
                'extra':float,
                'mta_tax':float,
                'tip_amount':float,
                'tolls_amount':float,
                'improvement_surcharge':float,
                'total_amount':float,
                'congestion_surcharge':float,
                'ehail_fee': float
            }
taxi_dtypes2 = {
                'VendorID': pd.Int64Dtype(),
                'passenger_count': pd.Int64Dtype(),
                'trip_distance': float,
                'RatecodeID':pd.Int64Dtype(),
                'store_and_fwd_flag':str,
                'PULocationID':pd.Int64Dtype(),
                'DOLocationID':pd.Int64Dtype(),
                'payment_type': pd.Int64Dtype(),
                'fare_amount': float,
                'extra':float,
                'mta_tax':float,
                'tip_amount':float,
                'tolls_amount':float,
                'improvement_surcharge':float,
                'total_amount':float,
                'congestion_surcharge':float,
                'airport_fee': float
            }
taxi_dtypes3 = {
                'PUlocationID': pd.Int64Dtype(),
                'DOlocationID': pd.Int64Dtype(),
                'SR_Flag': pd.Int64Dtype(),
                }
taxi_dtypes4 = {
                'PULocationID': pd.Int64Dtype(),
                'DOLocationID': pd.Int64Dtype(),
                'trip_miles': float,
                'trip_time': pd.Int64Dtype(),
                'base_passenger_fare': float,
                'tolls': float,
                'bcf': float,
                'sales_tax': float,
                'congestion_surcharge': float,
                'airport_fee': float,
                'tips': float,
                'driver_pay': float
                }

# getting green taxi in gcs
while start_dt <= end_dt:

    # string vars defined
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")

    # downloading file locally
    os.system(f'curl -O {url}')
    parquet_file = pq.ParquetFile(f'green_tripdata_{m_y}.parquet')

    # fetch by partition
    i = 1
    for batch in parquet_file.iter_batches():
        df = batch.to_pandas()
        print(f'fetched a df from iteration {i} with shape {df.shape}')

        # export correct pandas data types
        df = df.astype(taxi_dtypes1)

        # cleanup column names a bit
        df.columns = df.columns\
                    .str.replace('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', '_', regex=True)\
                    .str.lower()

        # add reporting month/year for later filtering out wrong records in dbt
        df['load_dt'] = [start_dt.strftime('%Y-%m-%d %H:%M:%S')] * len(df)

        # change time columns to right type
        df.lpep_pickup_datetime = df.lpep_pickup_datetime.apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))
        df.lpep_dropoff_datetime = df.lpep_dropoff_datetime.apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))

        root_path = f"{bucket_name}/{table_name_g}/{m_y}_{table_name_g}"
        print(f"loading parquets to {root_path} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

        # export to gcs
        table = pa.Table.from_pandas(df)
        gcs = pa.fs.GcsFileSystem()
        pq.write_to_dataset(
            table,
            root_path = root_path,
            filesystem = gcs
        )

        i += 1

    print('removing parquet from docker')

    os.remove(f'green_tripdata_{m_y}.parquet')

    start_dt += delta

# getting yellow taxi in gcs
while start_dt <= end_dt:

    # string vars defined
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")

    # downloading file locally
    os.system(f'curl -O {url}')
    parquet_file = pq.ParquetFile(f'yellow_tripdata_{m_y}.parquet')

    # fetch by partition
    i = 1
    for batch in parquet_file.iter_batches():
        df = batch.to_pandas()
        print(f'fetched a df from iteration {i} with shape {df.shape}')

        # export correct pandas data types
        df = df.astype(taxi_dtypes2)

        # cleanup column names a bit
        df.columns = df.columns\
                    .str.replace('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', '_', regex=True)\
                    .str.lower()

        # add reporting month/year for later filtering out wrong records in dbt
        df['load_dt'] = [start_dt.strftime('%Y-%m-%d %H:%M:%S')] * len(df)

        # change time columns to right type
        df.tpep_pickup_datetime = df.tpep_pickup_datetime.apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))
        df.tpep_dropoff_datetime = df.tpep_dropoff_datetime.apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))

        root_path = f"{bucket_name}/{table_name_y}/{m_y}_{table_name_y}"
        print(f"loading parquets to {root_path} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

        # export to gcs
        table = pa.Table.from_pandas(df)
        gcs = pa.fs.GcsFileSystem()
        pq.write_to_dataset(
            table,
            root_path = root_path,
            filesystem = gcs
        )

        i += 1

    print('removing parquet from docker')

    os.remove(f'yellow_tripdata_{m_y}.parquet')

    start_dt += delta

# getting fhv taxi in gcs
while start_dt <= end_dt:

    # string vars defined
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")

    # downloading file locally
    os.system(f'curl -O {url}')
    parquet_file = pq.ParquetFile(f'fhv_tripdata_{m_y}.parquet')

    # fetch by partition
    i = 1
    for batch in parquet_file.iter_batches():
        df = batch.to_pandas()
        print(f'fetched a df from iteration {i} with shape {df.shape}')

        # export correct pandas data types
        df = df.astype(taxi_dtypes3)

        # cleanup column names a bit
        df.columns = df.columns\
                    .str.replace('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', '_', regex=True)\
                    .str.lower()

        # add reporting month/year for later filtering out wrong records in dbt
        df['load_dt'] = [start_dt.strftime('%Y-%m-%d %H:%M:%S')] * len(df)

        # change time columns to right type
        df.pickup_datetime = df.pickup_datetime.apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))
        df.drop_off_datetime = df.drop_off_datetime.apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))

        root_path = f"{bucket_name}/{table_name_fhv}/{m_y}_{table_name_fhv}"
        print(f"loading parquets to {root_path} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

        # export to gcs
        table = pa.Table.from_pandas(df)
        gcs = pa.fs.GcsFileSystem()
        pq.write_to_dataset(
            table,
            root_path = root_path,
            filesystem = gcs
        )

        i += 1

    print('removing parquet from docker')

    os.remove(f'fhv_tripdata_{m_y}.parquet')

    start_dt += delta

# getting fhvhv taxi in gcs
while start_dt <= end_dt:

    # string vars defined
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")

    # downloading file locally
    try:
        os.system(f'curl -O {url}')
        parquet_file = pq.ParquetFile(f'fhvhv_tripdata_{m_y}.parquet')

        # fetch by partition
        i = 1
        for batch in parquet_file.iter_batches():
            df = batch.to_pandas()
            print(f'fetched a df from iteration {i} with shape {df.shape}')

            # export correct pandas data types
            df = df.astype(taxi_dtypes4)

            # cleanup column names a bit
            df.columns = df.columns\
                        .str.replace('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', '_', regex=True)\
                        .str.lower()

            # add reporting month/year for later filtering out wrong records in dbt
            df['load_dt'] = [start_dt.strftime('%Y-%m-%d %H:%M:%S')] * len(df)

            # change time columns to right type
            df.request_datetime = df.request_datetime.fillna(start_dt.strftime('%Y-%m-%d %H:%M:%S')).apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))
            df.on_scene_datetime = df.on_scene_datetime.fillna(start_dt.strftime('%Y-%m-%d %H:%M:%S')).apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))
            df.pickup_datetime = df.pickup_datetime.fillna(start_dt.strftime('%Y-%m-%d %H:%M:%S')).apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))
            df.dropoff_datetime = df.dropoff_datetime.fillna(start_dt.strftime('%Y-%m-%d %H:%M:%S')).apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))

            root_path = f"{bucket_name}/{table_name_fhvhv}/{m_y}_{table_name_fhvhv}"
            print(f"loading parquets to {root_path} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}")

            # export to gcs
            table = pa.Table.from_pandas(df)
            gcs = pa.fs.GcsFileSystem()
            pq.write_to_dataset(
                table,
                root_path = root_path,
                filesystem = gcs
            )

            i += 1

        print('removing parquet from docker')

        os.remove(f'fhvhv_tripdata_{m_y}.parquet')

        start_dt += delta
    except Exception as exc:
        print(f'error with {m_y}: {exc}')
        start_dt += delta
        continue
