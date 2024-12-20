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

    ```
    # open the jupyterlab from the python-hw6 container
    localhost:8888

    # pip install lib in the container 
    pip install kafka-python-ng
    ```
    - execute line 2-17 from `spark-streaming-hw6.py` in a jupyter notebook

    - answer: `True`

4. Sending data to the stream 

    - execute lines 20-33 from `spark-streaming-hw6.py` in a jupyter notebook

    - answer: `0.75 seconds`

    - to see the messages sent to topic create in Q2, in the `redpandas-1` container execute `rpk topic consume test-topic`

    


### Steps to run code 

1. copy dockerfile from week6 repo 

    ```
    cp ~/git_repos/data-engineering-zoomcamp/06-streaming/python/redpanda_example/docker-compose.yaml ~/git_repos/data-engineering-zoomcamp-2024/homeworks/hw6/.
    ```

2. build python image via command `docker build -f python-hw6.Dockerfile -t python-hw6 .` in this folder 

3. spin up the docker containers via `docker compose up -d` in this folder 

4. to get correct IP for redpandas container, fetch the value from `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' containerID` and update python script accordingly

### Helpful Links 

* [README.md](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/06-streaming/homework.md) page of questions 