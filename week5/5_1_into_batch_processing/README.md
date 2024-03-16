### Processing Data Methods

* two types: batch and streaming

* difference:

  - batch processing is when data is processed in a batch format, where the edges of the batch are defined by given parameters (usually start end time like day/week/hour etc)

  - streaming is more about processing in real time, where soon as records are created in a given source, they are extracted/processed and made available to the target audience

### Batch jobs essentials

* jobs are often done via scripts of various language:

  - python

  - SQL

  - Spark

  - FLINK

* typical workflow:

  1. fetch data from a given data lake (csv/parquets)

  2. load them on to remote storage (cloud buckets) via python usually

  3. use SQL to transform the data to a target format (dbt)

  4. Use Spark

  5. Use python

* workflows are usually orchestrated by a tool (ie Airflow, Mage or StepFunctions)

* advantage of workflow batches

  - easy to manage

  - easy to retry due to time intervals are fixed and not happening in real time

  - easy to scale (adjusting computing power/clustering)

* disadvatages

  - the data isn't available in real time so an end user might have to wait before they can use the target data

  - this can be resolved via streaming (but these cases are quite low)

* in industry see about batch vs streaming processing 80/20 occurance

### Helpful Links

* YT [lesson](https://www.youtube.com/watch?v=dcHe5Fl3MF8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=52)
