### Code execution steps 

1. copy over content from data talks repo to here:

    ```
    # create needed directories 
    cd ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/
    mkdir kafka
    mkdir json_example

    # copy over material 
    cd ~//git_repos/data-engineering-zoomcamp/06-streaming
    cp -r python/docker/kafka ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/kafka/.
    cp -r python/json_example ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/json_example/
    ```

2. create needed docker netowrk 

    ```
    # creates the network 
    docker network  create kafka-spark-network

    # verifies the network is there --> should be listed w/driver as bridge
    docker network ls 
    ```

3. go into the kafka folder and spin up the docker containers 

    ```
    # go to directory where docker-compose.yml is 
    cd kafka
    # run all the containers in detached mode 
    docker compose up -d
    ```

4. wait for the images to be pulled from docker image repo and then can see the containers up and running. this can be verified with `docker ps -a`

5. trigger `producer.py` to trigger the pipeline 

    ```
    cd json_example
    python producer.py
    ```

**--------------------------------------------------------AT MIN 21-------------------------------------------------------**

### Code overview 

* there are several services used in [docker-compose.yml](kafka/docker-compose.yml)

* services required for a successful kafka run: `broker`, `schema-registry`, `zookeeper`, `control-center`

* service `kafka-rest` is necessary for debugging purposes, this provides access to the API

* components needed in `docker-compose.yml`:

    + `broker` service: 

        ```
        # defines how kafka communicates within docker and how it can be accessed outside the docker 
        KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
        KAFKA_LISTENERS: PLAINTEXT://broker:29092,PLAINTEXT_HOST://broker:9092
        KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092
        KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
        ```

* [json_example/producer.py](json_example/producer.py):

    + the goal here is to read from `rides.csv` file and provide messages to a topic like a typical producer 

    + the topic is defined by [json_example/settings.py](json_example/settings.py)

    + seems that the data is fed to the kafka stream using the `KAFKA_LISTENERS` defined in the `broker` docker service. This is realized by the `BOOTSTRAP_SERVERS` in [json_example/settings.py](json_example/settings.py) and `config` object in [json_example/producer.py](json_example/producer.py)

    + it also sets up serialization for the messages to be later read by [json_example/consumer.py](json_example/consumer.py)

    + the serializer also converts message values to binary format (`utf-8`) for this is a requirement for kafka 

    + it sends the data to consumer via the class `Ride`, which is defined in [json_example/ride.py](json_example/ride.py)

* [json_example/ride.py](json_example/ride.py):

    + it just parses each of the messages provided by the producer script and formats it accordingly 

    + `__repr__` function is executed to print out the messages that are being parsed out by `Ride`. This is a way of QAing and debugging

* [json_example/consumer.py](json_example/consumer.py):

    + `config` object is using the same settings as in proucer (serializer, bootstrap, data type etc)

    + `auto_offset_reset` to determine which timepoint record to fetch. In the example here it is set to earliest, but usually in production this is set to latest 

    + for the deserialization of key and values, they are stored in kafka as binary format but must be converted back to regular format when entering python environemnt. This is why python int() function and `Ride` class from `rides.py` are used here 

    + foe line 25, this just prints out the messages that the consumer reads back from the stream, but this can be altered to transmit the results to another location (like a csv or to some kind of cloud location like BigQuery)

### Helpful Links 

* Youtube [lecture](https://www.youtube.com/watch?v=BgAlVknDFlQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=80)

* material for this lecture can be found in [06-streaming/python/docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/06-streaming/python/docker) directory 

* instructions for running [Pyspark Streaming](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/streams-example/pyspark/README.md)

* setup for running kafka and spark cluster on [docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/docker/README.md)