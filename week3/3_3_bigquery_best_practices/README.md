### Cost reduction 

* best to avoid queries like `select * `, best to specify column names 

    - this is because its column storage

    - `select * ` forces BigQuery to read all the columns and look into more detail than necessary

    - when the columns are specified in a select query, then the DWH doesn't need to read all the columns then therefor saving computing power 

- best to price the queries before running them (top right hand of the sql sheet)

- cluster/partition

- streaming inserts to be used with caution

- materialize result

    - when using a CTE for what ever given reason, if find that it is needed in multiple stages/tables, then best to materialize it so the DWH doesn't have to recalcualte it every time

### Optimize query performance 

- filter on partitioned/clustered columns 

- denormalize data 

- when have a complicated structure, best to use nested/repeated columns, will help denormalize data 

- not use external data source too much, will increase costs 

- dedup/reduce data before using it in a join 

- avoid oversharding tables 

    - sharding is applying horizontal partitioning, basically where each paritition has the same column structure, just row content varies from partition to partition. A bit of background can be provided [here](https://www.digitalocean.com/community/tutorials/understanding-database-sharding)

- when creating joins, best to have the from statement start with the largest table and then each consecutive join with slightly smaller ones till get to the end

    - first table it will be distributed evenly while the second table is broadcasted to all the nodes

### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit#slide=id.g10eebc44ce4_0_26)

* YT [video](https://www.youtube.com/watch?v=k81mLJVX08w)

* Query [sheet](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/03-data-warehouse/big_query.sql)