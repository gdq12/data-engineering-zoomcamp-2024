### Partitioning 

- can choose a time unit column or integer column 

- with time partition is by defult daily 

- choose more granular time sets if data is of larger volume and need to scan in more detail

- bigquery limits parition number by 4000

### Clustering 

- colocated centric, where the columns are matters

- the sort order is impacted by where the cluster column is 

- cluster tends to improve filtering and aggregation in queries 

- when the table size is less than 1 GB, not worth to partition and cluster because it doenst improve performance and it incures cost because it costs more for reading metadata and maintenance 

- can specif up to 4 clustering columns 

    - they must be top level and non-repated columns

    - can use various data types for clustering columns 

### Comparing the two 

- clustering cost ebenfits are unknown, but for partitioning one knows up front --> so partition is better if on a budget 

- clustering best when need more granularity than partitioning alone can provide 

- partition management very feasible, not possible with clustering really

- clustering allows for more advance filtering (where conditions) since one can create cluster on multiple columns, this can't be done with partitioning, since partitioning is allowed only on 1 column at a time

- best to use clustering when the cardinality of num values in column or group is large 

    - cardinality is the relationship a value in a column to other values of another column in another table (1-1, 1-many etc). Explanation comes from this [stackoverflow post](https://stackoverflow.com/questions/10621077/what-is-cardinality-in-databases)

- cluster over partition

    - when the data frame is too small, when each parition results in less than 1 GB of data per partition

    - if partitioning results in more than 4k partitions

    - if partitioning leads to constant mutations in many of the partitions (every few minutes for instance)

### Automatic reclustering 

- table is clustered --> new data is inserted into the table --> they are written into new blocks of the table --> they use key ranges that are already used by older/already created blocks --> this weakerns the sorting properties of the clustered table

- maintain performance --> BigQuery conducts periodic auto reclustering (this is done in the background)

- if a table is partitioned as well, the auto reclustering occurs within each partitioning --> meaning repartitioning doesn't occur 

- this auto reclustering has no additional cost

### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit#slide=id.g10eebc44ce4_0_26)

* YT [video](https://www.youtube.com/watch?v=-CqXf7vhhDs&t=3s)

* Query [sheet](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/03-data-warehouse/big_query.sql)