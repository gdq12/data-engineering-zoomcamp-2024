### Code execution steps

1. copy over content from data talks repo to here:

    ```
    # go over to needed directory 
    cd ~/git_repos/data-engineering-zoomcamp/06-streaming

    # copy over material 
    cp -r ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/kafka/ ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/kafka/.
    cp -r python/docker/spark ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/
    cp -r python/streams-example/pyspark ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/pyspark
    ```

2. build spark images 

    ```
    # go to shell script directory 
    cd ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/spark/

    # execute all the docker build commands via the shell script 
    ./build.sh
    ```

3. build python image

    ```
    # go to directory where docker file is 
    cd kafka/

    # build doker image 
    docker build -f python-wk6.Dockerfile -t python-wk6 .
    ```

4. create needed docker netowrk 

    ```
    # creates the network 
    docker network  create kafka-spark-network

    # verifies the network is there --> should be listed w/driver as bridge
    docker network ls 
    ```

5. create volume so sprak cluster logs can be stored in a specific folder 

    ```
    docker volume create --name=hadoop-distributed-file-system
    ```

6. spin up all the containers via docker compose up

    ```
    # go to directory where docker-compose.yml is 
    cd 6_14_pyspark_structured_streaming
    docker compose up -d
    ```

7. wait for the images to be pulled from docker image repo and then can see the containers up and running. this can be verified with `docker ps -a`

8. enter the python container to make sure all `*.py` files and `rides.csv` have been mounted into it via command `docker exec -it containerID sh`

9. execute the `producer.py` and `consumer.py` scripts within the python container to trigger the pipeline mechanism for the spark contianers 

    ```
    python3 producer.py

    python3 consumer.py
    ```

    + needed to update `BOOTSTRAP_SERVICES` for the correct broker IP. This was done with command `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID`

10. go through the jupyter notebook via `localhost:8888`

11. go through and review jupyter notebook `streaming-notebook.ipynb`

12. execute the pyspark-kafka python script via command `./spark-submit.sh streaming.py`

    + needed to update spark master IP in the shell file. This was done with command `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID`

13. when all is done, exit from containers opened (python a nd jupyter notebook) the `docker compose down`

### Code overview 

* require to create `docker volume` for spark containers, HDFS to store log files of sprak processes 

* [spark sub directory](spark)

    + faced issues with building the [spark/jupyterlab.Dockerfile](spark/jupyterlab.Dockerfile) when pip installing pyspark and jupyterlab libraries. Hypothesize because there is an issue installing python in a `eclipse-temurin` docker hub image from `cluster-base.Dockerfile`. Thus far this has been resolved by updating `jupyterlab.Dockerfile` to use `python:3.12` docker hub image instead and then installing needed libraries using `requirements.txt` from the same subdirectory 

### Review Pyspark syntax

* this was all executed in [pyspark/streaming-notebook.ipynb](pyspark/streaming-notebook.ipynb)

* `os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,org.apache.spark:spark-avro_2.12:3.5.3 pyspark-shell'`

    + this is for additional installations needed for pyspark to work with kafka

* pyspark reading kafka streams 

    ```
    df_kafka_raw = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092,broker:29092") \
        .option("subscribe", "rides_csv") \
        .option("startingOffsets", "earliest") \
        .option("checkpointLocation", "checkpoint") \
        .load()
    ```

    + `.option("subscribe", "rides_csv")` is to identify the topics that interested in 

    + `.option("checkpointLocation", "checkpoint")` is to keep track of what messages have or have not already read in 

* `df_kafka_raw.printSchema()`: apart from providing key/value info, it is also useful in providing some metadata that can be used for production performance analysis 

* Since kafka requires for key and values to be in binary format, `df_kafka_raw.selectExpr()` is used in pysprak to convert the binary characters to a more readable format 

* custom function `parse_ride_from_kafka_message()` is parse and convert to proper data types all the messages that have already been streamed by kafka 

* prior to inspecting the kafka data via `df_rides.show()`, must convert the streaming source to a data frame, so must use `writeStream`

* `writeStreams`

    + it has many possibility outputs. The stream outputs can be saved into a file or even store info back into kafka topics 

    + there is also the possibility to send the info to console or memory, this is done for debugging only though

    + timing of queries can be adjusted via `triggers` 

* `sink_console()` is a custom function that is meant to query kafka stream function in a set time interval. It will continue to query data until it is halted via `sink_console.stop()`

* `sink_memory()` is a cutsom function  that is meant to take query results and keep it in pyspark memory 

* what was elaborated in detail in the jupyter notebook is redone/coded in [pyspark/streaming.py](pyspark/streaming.py)

    + the script can't run successfully in python3 command line for it requires extra installations for pyspark to communicate/fetch from kafka, therefor it is better to execute `spark-submite.sh` shell script 

    + in the script, after it read the stream data and parses it for readable data types in spark, it queries kafka messages via `sink_console()` and then performs simple pyspark aggregations like groupbys and counts. The last part is kafka sink, where it takes one of the group by sinks and writes these stream results to a kafka topic. In order to do this (as elaborated in the jupyter notebook), the DF results must be transformed into a `value` part of a dictionary 

### Helpful Links 

* Youtube [lecture](https://www.youtube.com/watch?v=VIVr7KwRQmE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=80)

* material for this lecture can be found in [06-streaming/python/docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/06-streaming/python/docker) directory 

* instructions for running [Pyspark Streaming](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/streams-example/pyspark/README.md)

* setup for running kafka and spark cluster on [docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/docker/README.md)

* documentation on pyspark [sinks](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#output-sinks)

* documentation on pyspark [modes](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#output-modes)

* documentation on pyspark [triggers](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#triggers)

* documentation on pyspark [kafka sink](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#writing-data-to-kafka)