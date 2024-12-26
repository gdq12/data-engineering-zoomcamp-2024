### Advantages of ML in BigQuery 

* data ppl like data nalyst benefit from it 

* the advantage of this is that there isnt a large skill requirement (knowing python, R or java)

* there isnt memory limitation since it can all be done natively in BigQuery

* there isnt a need to export data into another python/R/java environment to build models 

### Steps in ML dev

1. collect data 

2. process data/feature engineering 

    + auto preprocessing: during model building BigQuery performs some transformations for missing value imputation and feature transformation. More details in the [documentation](https://cloud.google.com/bigquery/docs/auto-preprocessing)

    + manual preprocessing: customize which functioons can be applied to the data during or premodel buidling. Best to have more ML experience for these types of applications. More details in the [documentation](https://cloud.google.com/bigquery/docs/manual-preprocessing#types_of_preprocessing_functions)

3. split data into train/test set 

4. build/train model 

5. hypertuning model

6. validate model via different matrices 

### Review of provided queries 

* the goal is to predict the tip amount at the end of a journey 

* select the columns of interest for building the model and cast them to the appropriate data type so the model knows how to treat the features 

    ```
    CREATE OR REPLACE TABLE `taxi-rides-ny.nytaxi.yellow_tripdata_ml` (
    `passenger_count` INTEGER,
    `trip_distance` FLOAT64,
    `PULocationID` STRING,
    `DOLocationID` STRING,
    `payment_type` STRING,
    `fare_amount` FLOAT64,
    `tolls_amount` FLOAT64,
    `tip_amount` FLOAT64
    ) AS (
    SELECT passenger_count, trip_distance, cast(PULocationID AS STRING), CAST(DOLocationID AS STRING),
    CAST(payment_type AS STRING), fare_amount, tolls_amount, tip_amount
    FROM `taxi-rides-ny.nytaxi.yellow_tripdata_partitoned` WHERE fare_amount != 0
    )
    ```

    + casting location IDs as string infers to the model that these are category types and they should have `one-hot encoding` to applied to them 

* creating the model 

    ```
    CREATE OR REPLACE MODEL `taxi-rides-ny.nytaxi.tip_model`
    OPTIONS
    (model_type='linear_reg',
    input_label_cols=['tip_amount'],
    DATA_SPLIT_METHOD='AUTO_SPLIT') AS
    SELECT
    *
    FROM
    `taxi-rides-ny.nytaxi.yellow_tripdata_ml`
    WHERE
    tip_amount IS NOT NULL;
    ```

    + `input_label_col` is the feature that the model should predict 

    + `data_split_method` is to determine which ratio of the data should be training vs test data for the model 

* within BigQuery UI, can click on the model and look at it stats: what data its based on, how long did the model take to build, and statistics into its validity 

* check on the features:

    ```
    SELECT * FROM ML.FEATURE_INFO(MODEL `taxi-rides-ny.nytaxi.tip_model`);
    ```

    + this shows how each of the features in the data set were treated as by the model 

+ evaluating the model: 

    ```
    SELECT
    *
    FROM
    ML.EVALUATE(MODEL `taxi-rides-ny.nytaxi.tip_model`,
    (
    SELECT
    *
    FROM
    `taxi-rides-ny.nytaxi.yellow_tripdata_ml`
    WHERE
    tip_amount IS NOT NULL
    ))
    ```

    + evaluate model against the data set 

    + the stats provided help with finetuning the model 

* predicting or predict and explain 

    ```
    # predict only 
    SELECT
    *
    FROM
    ML.PREDICT(MODEL `taxi-rides-ny.nytaxi.tip_model`,
    (
    SELECT
    *
    FROM
    `taxi-rides-ny.nytaxi.yellow_tripdata_ml`
    WHERE
    tip_amount IS NOT NULL
    ))
    ```
    
    + just adds an extra column which is the predicted trip amount. Can also compare this to the actual tip_amount to see how the model faired

    ```
    SELECT
    *
    FROM
    ML.EXPLAIN_PREDICT(MODEL `taxi-rides-ny.nytaxi.tip_model`,
    (
    SELECT
    *
    FROM
    `taxi-rides-ny.nytaxi.yellow_tripdata_ml`
    WHERE
    tip_amount IS NOT NULL
    ), STRUCT(3 as top_k_features))
    ```

    + will indicate which top columns were used for the prediction 

    + this indication is provided at a row by row basis 

* hyper parameter tuning for improving the model 

    ```
    CREATE OR REPLACE MODEL `taxi-rides-ny.nytaxi.tip_hyperparam_model`
    OPTIONS
    (model_type='linear_reg',
    input_label_cols=['tip_amount'],
    DATA_SPLIT_METHOD='AUTO_SPLIT',
    num_trials=5,
    max_parallel_trials=2,
    l1_reg=hparam_range(0, 20),
    l2_reg=hparam_candidates([0, 0.1, 1, 10])) AS
    SELECT
    *
    FROM
    `taxi-rides-ny.nytaxi.yellow_tripdata_ml`
    WHERE
    tip_amount IS NOT NULL
    ```

    + there are various options that can be taken to remake the model and improve its performance

    + best to checkout the [create model page](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create) to see the full range of hypertuning possibilities
    

### Helpful Links

* Youtube [video](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse)

* starter [sql queries](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/03-data-warehouse/big_query_ml.sql)

* GCPs [intro doc](https://cloud.google.com/bigquery/docs/bqml-introduction) to ML and AI in BigQuery 

* GCP [hyper tuning parameter documentation](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm)

* GCPs [feature preprocessing documentation](https://cloud.google.com/bigquery/docs/preprocess-overview)