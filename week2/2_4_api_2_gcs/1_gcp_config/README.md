### Create GCP bucket 

* go to GCP console --> project dashboard --> cloud staorage page 

* `+ Create` create a new bucket named `mage-ny-taxi-tutorial`

    - for multi-region choose EU based 

    - everything else leave at default 

* create service account for mage 

    - `+ create service account` in service accounts 

    - name it `magic-zoomcamp` and give a description that it is for this specific lesson

    - make the role `owner` here so easier to make edits etc. In reality this should not be done.

### Mage cntainer Setup

* update mage container with credentials 

    - once this has been created need to fetch the key in json format --> move the downloaded file from downloads to `~/data-engineering-zoomcamp-2024/2_mage_repo` --> update `Dockerfile` and `docker-compose.yml` so it may be carried over in to the container 

    - update `io_config.yaml` so mage knows where to find the json file and fetch the appropriate credential in `GOOGLE_SERVICE_ACC_KEY_FILEPATH`

### Verifying GCP and Mage Contianer interactions 

* testing conections 

    * use the test_config pipeline to test it with `select 1` query 

    * to test connex to bucket, can run the example pipeline for the titanic dataset so the csv is loaded to local env --> drag drop the csv to GCP project bucket console --> run a data_loader (GCP storage) with update of `bucket_name` and `object_key` (filename) in script. 

### Helpful Links 

* Youtube [video](https://www.youtube.com/watch?v=00LP360iYvE&t=1s)