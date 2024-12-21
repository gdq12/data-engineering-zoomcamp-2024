import os 
import time 
import json
from pyspark.sql import SparkSession
from kafka import KafkaProducer

# get the start time of the script 
t0 = time.time()

# needed functions 
def prepare_df_to_kafka_sink(row, value_columns, key_column):
    keys, records = [], []
    keys.append({'key': str(row[key_column])})
    records.append({col: str(row[col]) for col in value_columns})
    return zip(keys, records)

def publish(producer, topic, records):
    for key_value in records:
        key, value = key_value
        try:
            producer.send(topic=topic, key=key, value=value)
            print(f"Producing record for <key: {key}, value:{value}>")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Exception while producing record - {value}: {e}")   
    producer.flush()

# needed vars 
url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet'
filename = 'green_tripdata_2019-10.parquet'

bootstrap_server = '172.19.0.3:29092' # update this based on: docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID
config = {'bootstrap_servers': bootstrap_server,
          'key_serializer': lambda x: json.dumps(x).encode('utf-8'),
          'value_serializer': lambda x: json.dumps(x).encode('utf-8')
         }

topic_name = 'green-trips'
value_columns = ['lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'passenger_count', 'trip_distance', 'total_amount']
key_column = 'VendorID'

# import parquet data into spark 
print('starting spark session')

spark = SparkSession.builder \
  .master("local[*]") \
  .appName('test') \
  .getOrCreate()

# os.system(f'curl -O {url}')

print(f'reading parquet {filename} to pyspark')
df = spark.read.parquet(filename)

# prep df for sending messages as producer
df_stream = prepare_df_to_kafka_sink(df, value_columns, key_column)

df_size = df.count()

# set up producer configuration
print(f'passing records to {topic_name} in redpanda')
producer = KafkaProducer(**config)
for i, row in zip(range(df_size), df.collect()):
    # parse keys and values from each row of RDD
    print(f'at row number {i+1} out of {df_size}')
    grn_records = prepare_df_to_kafka_sink(row, value_columns, key_column)
    # push messages to stream
    publish(producer, topic_name, grn_records)

# close session when job is done
spark.stop()

# get the time of the end of the script 
t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')