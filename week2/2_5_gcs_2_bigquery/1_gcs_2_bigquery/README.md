### I. Loading data from GCS and staging it 

- use `data loader` and `transformer` blocks 

- fetches the single parquet file from the bucket created in the previous lesson 

- stages the transformation by normalizing the column names: making all column names a single case and removing any possible spaces by replace them with underscores 

### II. Loading the data to BigQuery 

- this was done with a `data exporter` block, in this case chose an sql script but can be done with a python one as well 

    * perhaps python is a better one because easier to debug 

- with the sql one, the data from the previous block in the pipeline is called upon using jinja syntax: `select * from {{ df_1 }}`. The interphase indicates it before the script is executed

- provided schema and table name to create table in the background 

### Good to knows

- experienced strange behavior with the mage container runs. at times it either didn't load its native libraries properly or kept reading 0 records from the parquet file in the bucket even though there was data in there 

- to resolve, stop the container --> rebuild --> rerun 

- sometimes need a cleanup of the docker image local repo: `docker image prune -a`. this removes all images not used by a container. the suggestion came from [this article](https://www.baeldung.com/ops/docker-remove-dangling-unused-images)


### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=JKp_uzM-XsM&t=1s)