### I. Recreating a Pipeline 

- post creating a pipeline and namning it, can drag and drop blocks onto the pipeline editing space. 

- to sequentially links/organize the blocks, in tree mode can click and drag on the line links to the right posititions. 

- can also also have blocks run in parallel by adjusting the links between blocks in the tree view 

### II. Partition push data to GCS

- instead os pushing a single parquet file to the bucket, they can be paritioned by a column and chunk saved in a sub folder in the buket

- this can be done using `pyarrow`

- the data can be partitione by pickupdate (which is truncated to the day) and then push to gcs

- code is as follows:

    ```{python}
    import pyarrow as pa 
    import pyarrow.parquet as pq
    import os 

    if 'data_exporter' not in globals():
        from mage_ai.data_preparation.decorators import data_exporter

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/secret.json'

    bucket_name = 'mage-ny-taxi-tutorial'

    table_name = 'nyc_taxi_data'

    root_path = f'{bucket_name}/{table_name}'

    @data_exporter
    def export_data(data, *args, **kwargs):
        data['tpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date

        table = pa.Table.from_pandas(data)

        gcs = pa.fs.GcsFileSystem()

        pq.write_to_dataset(
            table, 
            root_path = root_path,
            partition_cols = ['tpep_pickup_date'],
            filesystem = gcs
        )
    ```


### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=w0XmcASRUnc&t=1s)