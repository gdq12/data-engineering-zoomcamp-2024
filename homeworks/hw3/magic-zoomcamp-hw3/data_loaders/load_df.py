import pandas as pd
import datetime
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    # month-year based on back fill adjustment of execution date 
    m_y_var = kwargs.get('execution_date').strftime("%Y-%m")

    # set up url for formatting 
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{m_y_var}.parquet'
    
    # hard code data types 
    taxi_dtypes = {
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
                    'congestion_surcharge':float
                }

    # import raw parquet data 
    print(f'fetching green taxi data from {m_y_var}')
    df = pd.read_parquet(url, engine = "fastparquet")

    # cutomize the data types 
    df = df.astype(taxi_dtypes)

    # convert time centric columns to correct type 
    df.lpep_pickup_datetime = df.lpep_pickup_datetime.apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))
    df.lpep_dropoff_datetime = df.lpep_dropoff_datetime.apply(lambda d: datetime.datetime.fromtimestamp(d.timestamp()).strftime('%Y-%m-%d %H:%M:%S'))

    print(f'fetched {df.shape[0]} records for {m_y_var}')

    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined' 