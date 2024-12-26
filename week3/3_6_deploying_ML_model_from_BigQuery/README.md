### Steps 

1. authenticate gcloud via CLI 

    ```
    gcloud auth login
    ```

2. copy the model into google cloud storage 

    ```
    bq --project_id taxi-rides-ny extract -m nytaxi.tip_model gs://taxi_ml_model/tip_model
    ```

3. copy the model from the bucket to a local temporary directory  

    ```
    mkdir /tmp/model

    gsutil cp -r gs://taxi_ml_model/tip_model /tmp/model
    ```

4. copy the model over to a local serving directory

    ```
    mkdir -p serving_dir/tip_model/1

    cp -r /tmp/model/tip_model/* serving_dir/tip_model/1
    ```

5. run the model in a tensorflow docker image 

    ```
    docker pull tensorflow/serving

    docker run -p 8501:8501 --mount type=bind,source=pwd/serving_dir/tip_model,target= /models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &
    ```

6. use [postman](https://www.postman.com/) to make some http requests (aka make a post request for prediction based on other feature values)

    ```
    curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_model:predict
    ```

7. when running postman locally then can visit the UI: `http://localhost:8501/v1/models/tip_model`


### Helpful Links

* Youtube [video](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse)

* steps to extract and deploy model in docker [doc](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/03-data-warehouse/extract_model.md)