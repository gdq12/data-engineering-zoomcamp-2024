### Code from lesson

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

# verify parquet read into spark successfully
df_grn.show()
df_grn.columns
df_grn.printSchema()

df_yellow.show()
df_yellow.columns
df_yellow.printSchema()

# rename some columns and create service_type column
df_grn = df_grn \
    .withColumnRenamed('lpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('lpep_dropoff_datetime', 'dropoff_datetime') \
    .withColumn('service_type', F.lit('green'))

df_yellow = df_yellow \
    .withColumnRenamed('tpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('tpep_dropoff_datetime', 'dropoff_datetime') \
    .withColumn('service_type', F.lit('yellow'))

# reshape dfs to get only common columns
com_col = list(set(df_grn.columns) & set(df_yellow.columns))

df_grn_sel = df_grn.select(com_col)
df_yellow_sel = df_yellow.select(com_col)

#combine the dfs together
df_trips_data = df_grn_sel.unionAll(df_yellow_sel)

# look into the data a bit
df_trips_data.groupBy('service_type').count().show()

# using spark sql

# define spark df as a temp table for the queries
df_trips_data.createOrReplaceTempView('trips_data')

# run a query and save it as a pandas df to execute head()
df_pd = df_result = spark.sql("""
SELECT
    -- Reveneue grouping
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month,
    service_type,

    -- Revenue calculation
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,
    SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
    AVG(passenger_count) AS avg_montly_passenger_count,
    AVG(trip_distance) AS avg_montly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3
""").toPandas()

df_pd.head(100)

# save the output as parquet files
df_result = df_result = spark.sql("""
SELECT
    -- Reveneue grouping
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month,
    service_type,

    -- Revenue calculation
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,
    SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
    AVG(passenger_count) AS avg_montly_passenger_count,
    AVG(trip_distance) AS avg_montly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3
""")

# save data according to the original partitions
df_result.write.parquet('summary_stats/')

# if want to save results into a single partition then add colaesce
df_result.coalesce(1).write.parquet('summary_stats/', mode = 'overwrite')
```

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=uAlp2VuZZPY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=58)
