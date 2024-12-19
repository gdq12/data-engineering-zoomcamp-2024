### Code execution steps

1. copy over content from data talks repo to here:

    ```
    # go over to needed directory 
    cd ~/git_repos/data-engineering-zoomcamp/06-streaming

    # copy over material 
    cp -r ~/git_repos/data-engineering-zoomcamp-2024/week6/6_13_streaming_with_python/kafka/ ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/kafka/.
    cp -r python/docker/spark ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/
    cp -r python/streams-example/pyspark ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/pyspark
    # cp -r python/json_example ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/
    # cp -r python/avro_example ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/.
    # cp -r java/kafka_examples/src/main/resources/rides.csv ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/json_example/.
    # cp python/requirements.txt ~/git_repos/data-engineering-zoomcamp-2024/week6/6_14_pyspark_structured_streaming/kafka/.
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

6. go into the kafka and spark folders to spin up the docker containers 

    ```
    # go to directory where docker-compose.yml is 
    cd kafka
    # run all the containers in detached mode 
    docker compose up -d

    # go to directory where docker-compose.yml is 
    cd spark
    # run all the containers in detached mode 
    docker compose up -d
    ```

5. wait for the images to be pulled from docker image repo and then can see the containers up and running. this can be verified with `docker ps -a`

6. enter the pythin container to make sure all `*.py` files and `rides.csv` have been mounted into it via command `docker exec -it containerID sh`

7. execute `python3 producer.py` to trigger the pipeline 

8. after all the `rides.csv` were exported as messages, can then trigger the consumer script via `python3 consumer.py`

**------------------------up to min 6 in video--------------------------------------------------------------------**


### Code overview 


### Helpful Links 

* Youtube [lecture](https://www.youtube.com/watch?v=VIVr7KwRQmE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=80)

* material for this lecture can be found in [06-streaming/python/docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/06-streaming/python/docker) directory 

* instructions for running [Pyspark Streaming](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/streams-example/pyspark/README.md)

* setup for running kafka and spark cluster on [docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/python/docker/README.md)