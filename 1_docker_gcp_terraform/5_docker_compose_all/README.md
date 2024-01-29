### I. Docker Compose Pipeline

1. Creating a docker network connects all the containers together, but to set this requires a bit of manual work, therefor a single yaml file can be created so to configure all containers ina single network

2. docker-compose.yaml structure
    
    ```bash
    services:
    	containerName:
    		image: imageName # to be pulled from docker hub
    		environment:
    			- var1=abc # variables needed for the container 
    		volumes:
    			- # local files that need to be mapped to directories in the container 
    		port:
    			- ####:#### # should be enclosed with quotation marks
    	containerName2:
    		....
    ```

3. Running the containers at once
    1. command to be executed in the same directory as the yaml file 
        
        ```{bash}
        # initiate containers
        docker-compose up

        # bring them back down 
        docker-compose down
        ```
        
    2. to stop all the containers: ctrl + c in same terminal
    3. have docker-compose run in the background of the same terminal (detached mode)
        
        ```bash
        docker-compose up -d
        ```
        
5. good to knows 
    1. when do a docker-compose up, its actually also building a docker network, can see those post the docker-compose up command via: docker network ls
    2. when logging back into pgAdmin web UI, must reconfigure the server, because not sure where to map configurations from postgresql docker to pgAdmin docker 
    3. the python docker wasnt included in the docker-compose because for a successful run the python must connect to the postgresql container after the postgresql has been created. Docker orchestration is complicated, better use tools like airflow or mage to facilitate this. 

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=hKI6PkPhpa0&t=1s)

* Lecturer's [notes](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)