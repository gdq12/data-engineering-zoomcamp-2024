### I. PgAdmin

- its a web based GUI

- info from pgAdmin site: https://www.pgadmin.org/download/pgadmin-4-container/

- will pgadmin docker to connect to postgresql docker 

    ``` {bash}
    docker run -it \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        dpage/pgadmin4
    ```
    * once the container has been initiated, can then visit the web GUI: localhost:8080

    * once in the docker required to create a new server: in the left column of the screen —> right click server —> register server
        1. General tab:
            1. name: local docker 
        2. Connection tab:
            1. host name/address: localhost
            2. port: 5432
            3. username: root
            4. password: root

    * when creating the server at first, wont be able to connect to postgres beacuse its looking for localhost in the same container that it is running, but postgresql is runing in another container. For this a container network must be created to facilitate this connectivity 

### II. Docker Network 

1. create/initiate the network 

    ```{bash}
    docker network create pg-network
    ```

2. initiate each of the containers (postgresql and pgAdmin)

    ```{bash}
    docker run -it \
        -e POSTGRES_USER="postgres" \
        -e POSTGRES_PASSWORD="root" \
        -e POSTGRES_DB="ny_taxi" \
        -v /Users/gdq/git_repos/data-engineering-zoomcamp-2024/1_docker_gcp_terraform/2_docker_sql/data \
        -p 5432:5432 \
        --network=pg-network \
        --name pg-database \
        --rm \
        postgres:13

    docker run -it \
        -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        --network=pg-network \
        --name pgAdmin \
        --rm \
        dpage/pgadmin4    
    ```

4. Configure within GUI interphase in browser

    1. create server 

        1. General tab:

            1. name: local docker 

        2. Connection tab:

            1. host name/address: pg-database

            2. port: 5432

            3. username: postgres

            4. password: root


### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=hCAIVe9N0ow&t=127s)

* Lecturer's [notes](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)