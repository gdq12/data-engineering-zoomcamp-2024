### I. Docker background pre-settings 

- Configurations set for this exercise in the docker-compose.yml file 

- There will be two containers that will work with each other: magic (mage) and postgres

### II. Setting up envs in Mage GUI
- Post the `docker compose up` many new files/directories are generated

- Directory composition good to knows 

    * Credentials: 
        + This is in the `magic-zoomcamp/io_config.yaml`

        + Can create multiple profiles and assign the needed credentials per profile: default vs dev 
        
        + Passing local credentials to mage files is done through jinja syntax (“{{env_var(‘VAR_NAME’’)}}”)

### III. Testing connection from Mage to postgres 

- Create a new pipeline 

- Go to the pipeline settings to rename it 

- Add a block to the pipeline: add a sql data loader 

- Run a query in the data loader interphase `select 1;` to test the cpnnection to postgres 

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=pmhI-ezd3BE)