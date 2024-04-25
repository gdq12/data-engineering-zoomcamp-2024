import argparse
import os
import pyspark
from pyspark.sql import SparkSession
from datetime import date
import datetime as datetime
from dateutil.relativedelta import relativedelta
from pyspark.sql import functions as F

# parsing input argumants from command line 
print('parsing input arguments')
parser = argparse.ArgumentParser()

parser.add_argument('--input_grn', required=True)
parser.add_argument('--input_yellow', required=True)
parser.add_argument('--output_name', required=True)

args = parser.parse_args()

# connect to a spark standalone cluster (get the cluster path from spark UI URL value)
spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

# assign temp bucket 
spark.conf.set('temporaryGcsBucket', 'dataproc-temp-europe-west10-837602464262-d7cfxcaf')

# read in the file to spark
print('reading parquets into python env')
df_grn = spark.read \
        .option("header", "true") \
        .parquet(args.input_grn)

df_yellow = spark.read \
            .option("header", "true") \
            .parquet(args.input_yellow)

# rename some columns and create service_type column
print('data wrangling the parquets a bit')
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
df_grn_sel.createOrReplaceTempView('grn_data')
df_yellow_sel.createOrReplaceTempView('yellow_data')

# create aggr DFs then join them
print('querying the wrangled parquet data')
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
print('joining the parquet summary stat data together')
df_join = df_grn_aggr2.join(df_yellow_aggr2, on = ['revenue_zone', 'revenue_month'], how = 'outer')

# export it to another parquet file
print('exporting to bigquery')
df_join.write.format('bigquery') \
  .option('table', args.output_name) \
  .save()