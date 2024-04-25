### Background of lesson

* instead of pushing data to a cloud bucket to then be pushed to BigQuery, it can be written directly into BigQuery instead.

* This is not necessarily ideal practice but a method interesting to explore

### Steps

1) push script from [5_13_create_local_cluster](../5_13_create_local_cluster) into a subfolder of the bucket that will work with

  ```
  # login and authenticate gcp creds (follow links and provide authentication codes when prompted)
  gcloud auth login
  gcloud auth application-default login

  # cp command
  gsutil cp vid13_wk5.py gs://spark-wk5-tutorial/scripts/vid13_wk5.py
  ```

2) grant the service account that Dataproc will work with to create tables in Bigquery

  ```{bash}
  gcloud projects add-iam-policy-binding project_id \
      --member=serviceAccount:project_id-compute@developer.gserviceaccount.com \
      --role="roles/bigquery.jobUser"

  ```

3) submit job command via SDK

  ``` {bash}
  gcloud dataproc jobs submit pyspark \
      --cluster=spark-wk5-cluster-v2 \
      --region=europe-west10 \
      --jars gs://spark-lib/bigquery/spark-3.4-bigquery-0.37.0.jar  \
      gs://spark-wk5-tutorial/scripts/vid13_wk5.py \
      -- \
        --input_grn=gs://spark-wk5-tutorial/grn_taxi_data/* \
        --input_yellow=gs://spark-wk5-tutorial/yellow_taxi_data/* \
        --output_name=ny_taxi_wk5_spark.summary_results_spark
  ```

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=HIm2BOj8C0Q&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=67)

* spark-biquery conenctor [documentation](https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example#pyspark)
