import os 
import time 
import json
from pyspark.sql import SparkSession
from kafka import KafkaProducer

# get the start time of the script 
t0 = time.time()

# needed functions 
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# needed vars 
url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet'
filename = 'green_tripdata_2019-10.parquet'

server = '172.19.0.2:29092' # update this based on: docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID

topic_name = 'green-trips'
value_columns = ['lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'passenger_count', 'trip_distance', 'total_amount']
key_column = 'VendorID'

# import parquet data into spark 
print('starting spark session')

spark = SparkSession.builder \
  .master("local[*]") \
  .appName('test') \
  .getOrCreate()

os.system(f'curl -O {url}')

print(f'reading parquet {filename} to pyspark')
df = spark.read.parquet(filename)

df_size = df.count()

# set up producer configuration
print(f'passing records to {topic_name} in redpanda')

# connecting to redpanda
producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)
producer.bootstrap_connected()

for i, row in zip(range(df_size), df.collect()):
    
    print(f'at row number {i+1} out of {df_size}')
    
    message = {col: str(row[col]) for col in value_columns}
    producer.send(topic_name, value=message)
    
    print(f"Sent: {message}")
    
producer.flush()

# close session when job is done
spark.stop()

# get the time of the end of the script 
t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')