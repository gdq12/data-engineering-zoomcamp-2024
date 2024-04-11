### Steps of a group by

1) Spark executes a query

2) sub results: will first filter down to needed data (1 executer per partition)

3) sub results: then will conduct group by (1 executer per partition)

4) stage 2: when each executor is done with the first stage group by, spark will reshuffle the records between partitions

  + there will be record keys per partition, they are a combination of the columns for the group by

  + spark reshuffle the records so that each partition has only 1 unique key

  + this type of reshuffling is known as external merge sort (algorithm for distributed sorted)

5) stage 2: group by again once all records are reshuffled

  + goal is to have only 1 record/row for a single key per the group by syntax

6) save to partitions

  + number of partitions can be defined in the write to parquet spark function

  + the re-merging of partitions requires reshuffling again

  + repartitioning is ok with a decent size of data, repartitioning and reshuffling is ill-advised when working with a much larger set of data

### Pyspark example code

``` {python}
df_yellow_revenue = spark.sql("""
SELECT
    date_trunc('hour', tpep_pickup_datetime) AS hour,
    PULocationID AS zone,

    SUM(total_amount) AS amount,
    COUNT(1) AS number_records
FROM
    yellow
WHERE
    tpep_pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2
""")

df_yellow_revenue \
    .repartition(20) \
    .write.parquet('data/report/revenue/yellow', mode='overwrite')
```

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=9qrDsY_2COo&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=59)
