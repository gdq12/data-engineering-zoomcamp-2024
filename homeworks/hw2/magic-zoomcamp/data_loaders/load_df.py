import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):

    # set up url for formatting 
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{}.csv.gz'
    
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

    # native date parsing 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    # fetching data for 3 months of 2020
    df_list = []
    for i in range(10, 13):
        print(f'fetching green taxi data from 2020-{i}')
        df = pd.read_csv(url.format(i)
                        , sep=','
                        , compression='gzip'
                        , dtype=taxi_dtypes
                        , parse_dates=parse_dates
                        )
        print(f'fetched {df.shape[0]} records for 2020-{i}')
        df_list.append(df)
    df = pd.concat(df_list, axis = 0)
    print(f'fetched all data with a shape of {df.shape}')
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'    