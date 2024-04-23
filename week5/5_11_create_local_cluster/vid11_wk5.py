#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

parser.add_argument('--input_start_date', required=True)
parser.add_argument('--input_end_date', required=True)

args = parser.parse_args()

# start spark stand alone cluster
## find out where spark is installed
print('initiating standalone clusters')
os.environ['SPARK_HOME']
## start the master cluster
os.system(f"{os.environ['SPARK_HOME']}/sbin/start-master.sh")
## start worker
os.system(f"{os.environ['SPARK_HOME']}/sbin/start-worker.sh spark://{os.environ['HOSTNAME']}:7077")

# connect to a spark standalone cluster (get the cluster path from spark UI URL value)
spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

# check working with the stand alone cluster
# spark

# create sub folder to download parquets into
os.system('mkdir /home/ubuntu/grn_taxi_data')
os.system('mkdir /home/ubuntu/yellow_taxi_data')

# download green taxi parquet files into folders
start_dt = datetime.datetime.strptime(args.input_start_date, '%Y-%m-%d').date()
end_dt = datetime.datetime.strptime(args.input_end_date, '%Y-%m-%d').date()

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
print('reading parquets into python env')
df_grn = spark.read \
        .option("header", "true") \
        .parquet('/home/ubuntu/grn_taxi_data/*')

df_yellow = spark.read \
            .option("header", "true") \
            .parquet('/home/ubuntu/yellow_taxi_data/*')

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
df_join.write.parquet('/home/ubuntu/summary_stats/total', mode = 'overwrite')

# stop spark session 
spark.stop()

# stop spark stand alone cluster and worker 
print('cleanning up the env a bit for a new run')
os.system(f"{os.environ['SPARK_HOME']}/sbin/stop-master.sh")
os.system(f"{os.environ['SPARK_HOME']}/sbin/stop-worker.sh spark://{os.environ['HOSTNAME']}:7077")

# cleanup the firectory a bit 
os.system('rm -r /home/ubuntu/grn_taxi_data')
os.system('rm -r /home/ubuntu/yellow_taxi_data')
os.system('rm -r /home/ubuntu/summary_stats')

