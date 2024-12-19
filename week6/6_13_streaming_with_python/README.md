### Code execution steps 

1. copy over content from data talks repo to here:

    ```
    # go over to needed directory 
    cd ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/

    # copy over material 
    cd ~/git_repos/data-engineering-zoomcamp/06-streaming
    cp -r python/docker/kafka ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/
    cp -r python/json_example ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/
    cp -r java/kafka_examples/src/main/resources/rides.csv ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/json_example/.
    cp python/requirements.txt ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/kafka/.
    ```

2. creating own python docker so not have to run python scripts in global environment

    ```
    # go to directory where docker file is 
    cd kafka/

    # build doker image 
    docker build -f python-wk6.Dockerfile -t python-wk6 .
    ```

3. create needed docker netowrk 

    ```
    # creates the network 
    docker network  create kafka-spark-network

    # verifies the network is there --> should be listed w/driver as bridge
    docker network ls 
    ```

4. go into the kafka folder and spin up the docker containers 

    ```
    # go to directory where docker-compose.yml is 
    cd kafka
    # run all the containers in detached mode 
    docker compose up -d
    ```

5. wait for the images to be pulled from docker image repo and then can see the containers up and running. this can be verified with `docker ps -a`

6. enter the pythin container to make sure all `*.py` files and `rides.csv` have been mounted into it via command `docker exec -it containerID sh`

7. trigger `producer.py` to trigger the pipeline 

8. after all the `rides.csv` were exported as messages, can then trigger the consumer script via `python3 consumer.py`

**---------------------------------------------------AT MIN 21-------------------------------------------------------**

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

    + `PLAINTEXT` --> `INTERNAL` and `PLAINTEXT_HOST` --> `EXTERNAL` to emphasize the purpose for each of the listeners. Listerners take messages from either inside or outside the docker network

    + for internal docker to docker communication, need to find the IP address of `broker`, this is elaborated below

* [json_example/producer.py](json_example/producer.py):

    + the goal here is to read from `rides.csv` file and provide messages to a topic like a typical producer 

    + the topic is defined by [json_example/settings.py](json_example/settings.py)

    + seems that the data is fed to the kafka stream using the `KAFKA_LISTENERS` defined in the `broker` docker service. This is realized by the `BOOTSTRAP_SERVERS` in `setting.py` and `config` object in `producer.py`

    + it also sets up serialization for the messages to be later read by [json_example/consumer.py](json_example/consumer.py)

    + the serializer also converts message values to binary format (`utf-8`) for this is a requirement for kafka 

    + it sends the data to consumer via the class `Ride`, which is defined in `ride.py`

* [json_example/ride.py](json_example/ride.py):

    + it just parses each of the messages provided by the producer script and formats it accordingly 

    + `__repr__` function is executed to print out the messages that are being parsed out by `Ride`. This is a way of QAing and debugging

* [json_example/consumer.py](json_example/consumer.py):

    + `config` object is using the same settings as in proucer (serializer, bootstrap, data type etc)

    + `auto_offset_reset` to determine which timepoint record to fetch. In the example here it is set to earliest, but usually in production this is set to latest 

    + for the deserialization of key and values, they are stored in kafka as binary format but must be converted back to regular format when entering python environemnt. This is why python int() function and `Ride` class from `rides.py` are used here 

    + for line 25, this just prints out the messages that the consumer reads back from the stream, but this can be altered to transmit the results to another location (like a csv or to some kind of cloud location like BigQuery)

* python docker added to network 

    + [kafka/python-wk6.Dockerfile](kafka/python-wk6.Dockerfile) and [kafka/requirements.txt][kafka/requirements.txt] where created for this 

    + an updated version of `requirements.txt` was created and commited since a new solution was required for kafka to work with pytho 3.12, [solution3 stackoverflow](https://stackoverflow.com/questions/77287622/modulenotfounderror-no-module-named-kafka-vendor-six-moves-in-dockerized-djan) details this. Getting an updated version of `requirements.txt`. This was done by after python docker container being updated, `pip freeze > requirements.txt` executed in the running container and then it was exported via `docker cp containerID:/home/ubuntu/requirements.txt ~/file/destination/path`

* These scripts were adapted in that python scripts are executed from a python docker container within the same network so as to not have to configure the python global env for the script run. In order to successfully carry this out the kafka internal listener address had to be identified and updated accordingly in `settings.py` for value `BOOTSTRAP_SERVERS`. The broker kafka running docker IP address was obtained by the following docker command:

    ```
    docker inspect \
    -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID
    ```

    + so far it seems that the IP address is always `172.18.0.3`, though should this change the current IP address can be obtained from the command above afer `docker compose up -d` command

    + a pretty good elaboration of this can be found in a [kaaiot article](https://www.kaaiot.com/blog/kafka-docker) and [confluent page](https://www.confluent.io/blog/kafka-listeners-explained/)

    + perhaps to explore in the future to fix IP addresses in a docker network would be this [medium article](https://medium.com/@wandrys.sousa/assign-a-fixed-ip-address-to-a-container-in-docker-compose-2cc6c1a6151e)


### Helpful Links 

* Youtube [lecture](https://www.youtube.com/watch?v=BgAlVknDFlQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=80)

* material for this lecture can be found in [06-streaming/python/docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/06-streaming/python/docker) directory 

* instructions for running [Pyspark Streaming](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/streams-example/pyspark/README.md)

* setup for running kafka and spark cluster on [docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/docker/README.md)

* background on [kafka listeners](https://www.confluent.io/blog/kafka-listeners-explained/)