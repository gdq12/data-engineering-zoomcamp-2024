# Q3
import json
import time 

from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = '172.19.0.2:29092'

producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

producer.bootstrap_connected()

# Q4
t0 = time.time()

topic_name = 'test-topic'

for i in range(10):
    message = {'number': i}
    producer.send(topic_name, value=message)
    print(f"Sent: {message}")
    time.sleep(0.05)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')

# import grn taxi data 
import os 
from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .master("local[*]") \
  .appName('test') \
  .getOrCreate()

os.system('curl -O https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-10.parquet')

df = spark.read.parquet('fhv_tripdata_2019-10.parquet')

for row in df.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}
    print(row_dict)
    break