### Spark Clusters

* Locally: Cluster consists of single/multiple executors that execute tasks based on the developed code

* Components of a spark cluster

  - Master:

    + A drive (Airflow, PC, cloud machine) sends code/instructions from pyspark

    + Orchestrates jobs based on package, the progress of this can be seen in the UI by going to localhost:4040

  - Executors

    + Machines that perform computations

    + They are orchestrated by the Master

* When a given executor finishes a tasks, the Master realizes this and assigns it a new task based on what the packages requires
When working with parquet files, they are partitioned. This leads to having a dedicated executor per partition to perform the required tasks



### Helpful Links

* YT [video](https://www.youtube.com/watch?v=68CipcZt7ZA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=59)
