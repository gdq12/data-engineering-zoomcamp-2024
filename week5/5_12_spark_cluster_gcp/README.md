### Google Cloud Platforms Dataproc w/Spark

1) in GCP dashboard search for dataproc API --> enable it

2) go to Dataproc page and create a cluster:

  + `+ Create Cluster`

  + `Cluster on Computer Engine`

  + fill out fields:

    * set up cluster tab:

      - Name: spark-wk5-cluster

      - Region: europe-west10 (same region as bucket)

      - Cluster type: Single Node (use this when working with a small amount of data)

      - optional components: jupyter notebook, docker

    * customize cluster (optional) tab:

      - uncheck "Configure all instances to have only internal IP address"

  + good to know: can also see the cluster instance in `VM Instances` page of the dashboard

3) push script from [5_11_create_local_cluster](../5_11_create_local_cluster) into a subfolder of the bucket that will work with

  ```
  # login and authenticate gcp creds (follow links and provide authentication codes when prompted)
  gcloud auth login
  gcloud auth application-default login

  # cp command
  gsutil cp vid12_wk5.py gs://spark-wk5-tutorial/scripts/vid12_wk5.py
  ```

4) Submit a job in the cluster

  * there are 3 methods of submitting jobs to Dataproc: UI, GCP SDK and REST API

  I. First method via UI:

    + select desired cluster (from step2)

    + `+ SUBMIT JOB`

    + Job type: `PySpark`

    + main python file: `gs://spark-wk5-tutorial/scripts/vid12_wk5.py`

    + Arguments: `--input_grn=gs://spark-wk5-tutorial/grn_taxi_data/*`, `--input_yellow=gs://spark-wk5-tutorial/yellow_taxi_data/*`, `--output_path=gs://spark-wk5-tutorial/vid12_results`

  II. Second method via SDK (in the docker container terminal)

    + authorize the service account the docker container is running under to work with Dataproc

      ``` {bash}
      gcloud projects add-iam-policy-binding 837602464262 \
          --member=serviceAccount:magic-zoomcamp@ny-taxi-412905.iam.gserviceaccount.com \
          --role="roles/dataproc.worker"
      ```

    * run bash command in docker container to send job

      ``` {bash}
      # set project env var in docker container
      gcloud config set project projectName

      # cmd for sending job
      gcloud dataproc jobs submit pyspark \
          --cluster=spark-wk5-cluster-v2 \
          --region=europe-west10 \
          gs://spark-wk5-tutorial/scripts/vid12_wk5.py \
          -- \
            --input_grn=gs://spark-wk5-tutorial/grn_taxi_data/* \
            --input_yellow=gs://spark-wk5-tutorial/yellow_taxi_data/* \
            --output_path=gs://spark-wk5-tutorial/vid12_results
      ```

### Good to know

* can sometimes come across permission errors with service accounts for the cluster. service account background can be found [here](https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/service-accounts#VM_service_account).

* easiest way to grand correct permission is via gcp shell terminal and execute the following:

  ``` {bash}
  gcloud projects add-iam-policy-binding project_number \
      --member=serviceAccount:project_number-compute@developer.gserviceaccount.com \
      --role="roles/dataproc.worker"
  ```

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=osAiAYahvh8&list=PL3MmuxUbc  _hJed7dXYoJw8DoCuVHhGEQb&index=67)

* dataproc service accounts [trouble shooting](https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/service-accounts#VM_service_account)

* dataproc submit a job via DSK [documentation](https://cloud.google.com/dataproc/docs/guides/submit-job)
