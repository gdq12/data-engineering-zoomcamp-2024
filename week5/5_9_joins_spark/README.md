### Python Code

``` {python}
# import needed libraries
import os
import pyspark
from pyspark.sql import SparkSession
from datetime import date
import datetime as datetime
from dateutil.relativedelta import relativedelta
from pyspark.sql import functions as F

# connect to a spark session
spark = SparkSession.builder \
  .master("local[*]") \
  .appName('test') \
  .getOrCreate()

# create sub folder to download parquets into
!mkdir grn_taxi_data
!mkdir yellow_taxi_data

# download green taxi parquet files into folders
start_dt = date(2020, 1, 1)
end_dt = date(2021, 12, 31)
delta = relativedelta(months=1)

os.chdir(f'/home/ubuntu/grn_taxi_data/')
while start_dt <= end_dt:

    # string vars defined
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")

    # downloading file locally
    os.system(f'curl -O {url}')
    start_dt += delta

# download yellow taxi parquet files into folders
start_dt = date(2020, 1, 1)
end_dt = date(2021, 12, 31)
delta = relativedelta(months=1)

os.chdir(f'/home/ubuntu/yellow_taxi_data/')
while start_dt <= end_dt:

    # string vars defined
    m_y = start_dt.strftime("%Y-%m")
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{m_y}.parquet'
    print(f"getting parquet for {m_y} on {datetime.datetime.now().strftime('%B %d, %Y %H:%M:%S')}: {url}")

    # downloading file locally
    os.system(f'curl -O {url}')
    start_dt += delta

# read in the file to spark
df_grn = spark.read \
        .option("header", "true") \
        .parquet('/home/ubuntu/grn_taxi_data/*')

df_yellow = spark.read \
            .option("header", "true") \
            .parquet('/home/ubuntu/yellow_taxi_data/*')

# rename some columns and create service_type column
df_grn = df_grn \
    .withColumnRenamed('lpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('lpep_dropoff_datetime', 'dropoff_datetime')

df_yellow = df_yellow \
    .withColumnRenamed('tpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('tpep_dropoff_datetime', 'dropoff_datetime')

# reshape dfs to get only common columns
com_col = list(set(df_grn.columns) & set(df_yellow.columns))

df_grn_sel = df_grn.select(com_col)
df_yellow_sel = df_yellow.select(com_col)

# define spark df as a temp table for the queries
df_grn.createOrReplaceTempView('grn_data')
df_yellow.createOrReplaceTempView('yellow_data')

# create aggr DFs then join them
df_grn_aggr = spark.sql("""
SELECT
    -- Reveneue grouping
    PULocationID AS revenue_zone,
    date_trunc('hour', pickup_datetime) AS revenue_month,

    SUM(total_amount) AS revenue,
    COUNT(1) AS number_records
FROM
    grn_data
WHERE
    pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2
""")

df_yellow_aggr = spark.sql("""
SELECT
    -- Reveneue grouping
    PULocationID AS revenue_zone,
    date_trunc('hour', pickup_datetime) AS revenue_month,

    SUM(total_amount) AS revenue,
    COUNT(1) AS number_records
FROM
    yellow_data
WHERE
    pickup_datetime >= '2020-01-01 00:00:00'
GROUP BY
    1, 2
""")

# rename columns for join
df_grn_aggr2 = df_grn_aggr \
    .withColumnRenamed('revenue', 'green_amount') \
    .withColumnRenamed('number_records', 'grn_row_num')

df_yellow_aggr2 = df_yellow_aggr \
    .withColumnRenamed('revenue', 'yellow_amount') \
    .withColumnRenamed('number_records', 'yellow_row_num')

# conduct an outer join to verify all records are accounted for
df_join = df_grn_aggr2.join(df_yellow_aggr2, on = ['revenue_zone', 'revenue_month'], how = 'outer')

# df_join.show()

# export it to another parquet file
df_join.write.parquet('summary_stats/total', mode = 'overwrite')

# fetch the zone data
url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
os.system(f'curl -O {url}')

df_zones = spark.read \
        .option("header", "true") \
        .csv('taxi_zone_lookup.csv')

df_zones.show()

# join the df_join with the zone table
df_result = df_join.join(df_zones, df_join.revenue_zone == df_zones.LocationID) \
            .drop('LocationID', 'zone')

# df_result.show()

df_result.write.parquet('summary_stats/total_w_zone_names', mode = 'overwrite')
```

### Steps during joins

There are several steps that take place during these lines of code:

``` {python}
# rename columns for join
df_grn_aggr2 = df_grn_aggr \
    .withColumnRenamed('revenue_amount', 'green_amount') \
    .withColumnRenamed('number_records', 'grn_row_num')

df_yellow_aggr2 = df_yellow_aggr \
    .withColumnRenamed('revenue_amount', 'yellow_amount') \
    .withColumnRenamed('number_records', 'yellow_row_num')

# conduct an outer join to verify all records are accounted for
df_join = df_grn_aggr2.join(df_yellow_aggr2, on = ['revenue_zone', 'revenue_month'], how = 'outer')

df_join.show()
```

1) the group bys are performed per df table (if this is materialized already into parquets then this step can be skipped)

2) then it conducts the joins

  + the join needs to create complex records, where the key will become the combo of the join columns

  + the records will be reshuffled into new partitions where that each partition will consists of only a unique single key

  + then it will try to reduce records by creating new records that are a combo of records from the previous DFs with the same key

  + the type of join dictates what type of record reduction occurs: outer join include all records while inner join only keep records that are sourced from both DFs

### Joining parquets of different sizes

This is based on the following code:

```{python}
# fetch the zone data
url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
os.system(f'curl -O {url}')

df_zones = spark.read \
        .option("header", "true") \
        .csv('taxi_zone_lookup.csv')

df_zones.show()

# join the df_join with the zone table
df_result = df_join.join(df_zones, df_join.revenue_zone == df_zones.LocationID) \
            .drop('LocationID', 'zone')

# df_result.show()

df_result.write.parquet('summary_stats/total_w_zone_names', mode = 'overwrite')
```

* the execution plan for these type of joins are different (broken up into more than 1 step) is due to a step known as "broadcast exchange"

* theoretical background of what is happening:

  + for the lasrge DF, each executor works with each partition

  + since the small DF is quite small in size, instead of getting its own executor it is "broadcasted" to each executor already working with the different partitions. The small DF is being copied over to each executor

  + the join then occurs within each executor, there is no need to reshuffle records around


### Helpful Links

* YT [video](https://www.youtube.com/watch?v=lu7TrqAWuH4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=60)
