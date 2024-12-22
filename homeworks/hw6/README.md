### Q&As

1. whats the version of the redpandas-1 container 

    ```
    # enter running container 
    docker exec -it contianerID sh

    # get help for rpk CLI commands
    rpk help 

    # get the rdk version 
    rpk --version
    ```

    - answer: `rpk version v23.2.26 (rev 328d83a06e)`

2. create a topic using rpk and save output 

    ```
    # craete the topic 
    rpk topic create test-topic

    # verify the topic was created 
    rpk topic list
    ```

    - answer: `TOPIC: test-topic, STATUS: OK`

3. connecting to the kafka server 

    - terminal:

        ```
        # open the jupyterlab from the python-hw6 container
        localhost:8888

        # pip install lib in the container 
        pip install kafka-python-ng
        ```
    
    - pyhton/jupyter notebook:

        ```
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
        ```

    - answer: `True`

4. Sending data to the stream 

    - python/jupyter notebook lines:

        ```
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
        ```

    - answer: `0.75 seconds`

    - to see the messages sent to topic create in Q2, in the `redpandas-1` container execute `rpk topic consume test-topic`. 
    
    - To see the constant new messages the consumer reads, re-execute the last python lines mentioned here in the python container several times and see the redpandas-1 terminal being constantly updated

    - iterating through the taxi data

        + downloaded the parquet from the official website as opposed to the csv from datatalk module page

        + had to adapt the iteration of a spark DF by using the `collect()` function 

        + python code used in the end 

            ```
            # import grn taxi data 
            import os 
            from pyspark.sql import SparkSession

            spark = SparkSession.builder \
            .master("local[*]") \
            .appName('test') \
            .getOrCreate()

            os.system('curl -O https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet')

            df = spark.read.parquet('green_tripdata_2019-10.parquet')

            # iterating through the taxi data 
            def spark_serializer(x):
                VendorID=x.VendorID
                lpep_pickup_datetime=x.lpep_pickup_datetime
                lpep_dropoff_datetime=x.lpep_dropoff_datetime
                PULocationID=x.PULocationID
                DOLocationID=x.DOLocationID
                passenger_count=x.passenger_count
                trip_distance=x.trip_distance
                tip_amount=x.tip_amount
                return (VendorID, lpep_pickup_datetime, lpep_dropoff_datetime, PULocationID, DOLocationID, passenger_count, trip_distance, tip_amount)

            for row in df.collect():
                print(spark_serializer(row))
                break
                
            # close the spark session 
            spark.stop()
            ```

5. Sending the trip data 

    - create topic in `redpanda-1` via command `rpk topic create green-trips`   

    -  execute script `producer.py`, it took `501.53 seconds`

    - create a pyspark consume python lines:

        ```
        from time import sleep
        import pyspark
        from pyspark.sql import SparkSession

        pyspark_version = pyspark.__version__
        kafka_jar_package = f"org.apache.spark:spark-sql-kafka-0-10_2.12:{pyspark_version}"

        spark = SparkSession \
            .builder \
            .master("local[*]") \
            .appName("GreenTripsConsumer") \
            .config("spark.jars.packages", kafka_jar_package) \
            .getOrCreate()

        # connect to stream 
        server = '172.19.0.3:29092' # update this based on: docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID

        green_stream = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", server) \
            .option("subscribe", "green-trips") \
            .option("startingOffsets", "earliest") \
            .load()

        # check to see if a record can be picked up by the live stream
        def peek(mini_batch, batch_id):
            first_row = mini_batch.take(1)

            if first_row:
                print(first_row[0])

        query = green_stream.writeStream.foreachBatch(peek).start()

        # execute to stop printing out messages 
        query.stop()

        spark.stop()
        ```

        + one of the outputs for the last code above: `Row(key=None, value=bytearray(b'{"lpep_pickup_datetime": "2019-10-01 00:26:02", "lpep_dropoff_datetime": "2019-10-01 00:39:58", "PULocationID": "112", "DOLocationID": "196", "passenger_count": "1.0", "trip_distance": "5.88", "total_amount": "19.3"}'), topic='green-trips', partition=0, offset=0, timestamp=datetime.datetime(2024, 12, 22, 11, 13, 11, 346000), timestampType=0)`

6. Parsing the data 

    - python code executed in jupyter notebook 

        ```
        from time import sleep
        import pyspark
        from pyspark.sql import SparkSession

        pyspark_version = pyspark.__version__
        kafka_jar_package = f"org.apache.spark:spark-sql-kafka-0-10_2.12:{pyspark_version}"

        spark = SparkSession \
            .builder \
            .master("local[*]") \
            .appName("GreenTripsConsumer") \
            .config("spark.jars.packages", kafka_jar_package) \
            .getOrCreate()

        # connect to stream 
        server = '172.19.0.2:29092' # update this based on: docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID

        green_stream_raw = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", server) \
            .option("subscribe", "green-trips") \
            .option("startingOffsets", "earliest") \
            .load()


        from pyspark.sql import types

        col_list = ["lpep_pickup_datetime", "lpep_dropoff_datetime", "PULocationID", "DOLocationID", "passenger_count", "trip_distance", "tip_amount"]
        schema = types.StructType() \
            .add("lpep_pickup_datetime", types.StringType()) \
            .add("lpep_dropoff_datetime", types.StringType()) \
            .add("PULocationID", types.IntegerType()) \
            .add("DOLocationID", types.IntegerType()) \
            .add("passenger_count", types.DoubleType()) \
            .add("trip_distance", types.DoubleType()) \
            .add("tip_amount", types.DoubleType())


        from pyspark.sql import functions as F

        # set up query to to structure stream data 
        green_stream = green_stream_raw \
        .select(F.from_json(F.col("value").cast('STRING'), schema).alias("data")) \
        .select("data.*") 
        # .filter(F.col("PULocationID") > 0)

        # quick inspection of the schema for each of the stream connex objects 
        green_stream_raw.printSchema()
        green_stream.printSchema()

        # take a look at what pickup from stream based on specific time frames 
        green_stream.writeStream \
            .outputMode("append") \
            .trigger(processingTime="10 minutes") \
            .format("console") \
            .option("truncate", False) \
            .start()
        ```

        - to make sure the `green_stream` object is successfully created, need to make sure the `writeStream()` from the previous question was already executed for it auto parses out the message from redpandas value part of the json. 

        - the `writeStream()` permitted to pick up some stream data, but all values were null, quite strange but perhaps it has to do with a lot of trial and error with populating the producer and fixing the pyspark consumer, perhaps a whole new spin up of the containers for a new run will fix this. 

7. Most popular destination 

    - to be done in a future date. think need to review module 5/6 and 2nd workshop to better complete this homework. there are currently too many doubt and deviations from suggested answers to mark this complete


### Steps to run code 

1. `docker-compose.yaml` is based on the [redpanda example](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/redpanda_example/docker-compose.yaml)

2. build python image via command `docker build -f python-hw6.Dockerfile -t python-hw6 .` in this folder 

3. spin up the docker containers via `docker compose up -d` in this folder 

4. to get correct IP for redpandas container, fetch the value from `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID` and update python script accordingly

### Helpful Links 

* [README.md](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/06-streaming/homework.md) page of questions 

* brief overview of redpanda streaming provided by [Data Talks Club](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/06-streaming/python/redpanda_example)

* [getting started redpanda blog post](https://www.redpanda.com/blog/get-started-rpk-manage-streaming-data-clusters) CLI centric 