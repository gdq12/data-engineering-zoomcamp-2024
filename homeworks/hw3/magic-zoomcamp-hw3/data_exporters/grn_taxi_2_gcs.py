import pyarrow as pa 
import pyarrow.parquet as pq
import os 

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/ny-taxi-412905-ac957361bbc4.json'

bucket_name = 'mage-ny-taxi-hw3'

table_name = "nyc_green_taxi_data"

@data_exporter
def export_data(data, *args, **kwargs):
    
    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    root_path = f"{bucket_name}/{kwargs.get('execution_date').date()}_{table_name}"

    print(f'loading parquets to {root_path}')

    pq.write_to_dataset(
        table, 
        root_path = root_path,
        filesystem = gcs
    )