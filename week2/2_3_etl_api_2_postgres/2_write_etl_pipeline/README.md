### I. Setting up the pipeline 

1. create a new standard (batch) pipeline

2. rename in settings to `api_2_postgres`

### II. Blocks of the Pipeline

1. create a new block (data loader): python --> api

    * update the script to the following [python script](https://github.com/mage-ai/mage-zoomcamp/blob/solutions/magic-zoomcamp/data_loaders/load_nyc_taxi_data.py). main take aways from this:

    * prior to defining the function, the script verifies the correct modules are loaded from the docker containers environment (lines 4-7).
    
    * map data types so it can be pushed easily to postgres (optimizes memory consumption). Also, if the data types of the input file ever change, then the job will fail and will be notified (thats a good thing). 

    * the test function at the bottom determines if the previous function produced a dataframe or not, asserts an exception if the previous function fails to return a df. 

2. once the load script is successfully run then can create a transformation script: 

    * at the bottom of the `load_2_postgres.py` script click on `tranformation` and create a new pyton script called `transform_taxi_data.py`

    * in this transformation the rows where passenger_count = 0 is removed since this is logocally not possible. 

    * since `pandas` library was already loaded in the previous script, it is still in the global envirnment and doesn't have to be loaded again (possible explanation?)

    * any functions that proceeds the data-dentric function that is decorated with `@test` is an assertion. also good to know that any function with this decorator will be passed a df. 

3. once the tranformation script has succesfully run can add a data exporter script at the bottom and name the python script `taxi_data_2_postgres.py`

    * the data expoerter template for postgres already comes well formated. 

    * important field is `config_profile` so can choose which credential defined in the `io_config.yaml` to use. 

4. can check the data that was just loaded to postgres by using an sql data loader script `check_on_postgres_data.sql` 

    * can do checks like:

        + `select count(*) from ny_taxi.yellow_taxi_data` to verify all records were imported to postgres 

        + `select * from ny_taxi.yellow_taxi_data where passenger_count = 0` to verify the data transformation script correctly filtered out unwanted records 

### Helpful Links 

* Youtube [video](https://www.youtube.com/watch?v=Maidfe7oKLs&t=17s)

* Example data load block [python script](https://github.com/mage-ai/mage-zoomcamp/blob/solutions/magic-zoomcamp/data_loaders/load_nyc_taxi_data.py)