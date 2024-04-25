# import needed libraries
import os
import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from datetime import date
import datetime as datetime
from pyspark.sql import functions as F

# connect to a spark session
spark = SparkSession.builder \
  .master("local[*]") \
  .appName('test') \
  .getOrCreate()

## Q1: install spark and pyspark --> get version
spark.version

# downnload the FHV oct 2019 file and repartition it into 6 parquets. what is the average size of each?
os.system('curl -O https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-10.parquet')

df = spark.read.parquet('fhv_tripdata_2019-10.parquet')

# check on components of parquet
df.dtypes

df.show()

# repartition data
df.repartition(6).write.parquet('repartitioned_data/', mode = 'overwrite')

# check partition sizes
os.system('ls -la repartitioned_data/')

## Q3. How many taxi trips were there on the 15th of October?
# method1: pyspark
df.filter(F.date_trunc('dd', df.pickup_datetime) == F.lit("2019-10-15")).count()

# method2: spark sql
df.createOrReplaceTempView('fhv_trip_data')

spark.sql(""" select count(*)
from fhv_trip_data
where date_trunc('dd', pickup_datetime) = '2019-10-15'
""").show()

## Q4. what is the length of the longest trip in the dataset in hours
# method1 spark sql
spark.sql("""select pickup_datetime, dropOff_datetime
, (unix_timestamp(dropoff_datetime)-unix_timestamp(pickup_datetime))/(3600)diff_hours
from fhv_trip_data
where date_trunc('mm', pickup_datetime) >= '2019-10-01'
and date_trunc('mm', dropOff_datetime) <= '2019-10-31'
and dropOff_datetime > pickup_datetime
order by 3 desc
""").show()

## method2 using pyspark filtering and functions
df.filter(F.date_trunc('dd', df.pickup_datetime) >= F.lit("2019-10-01")) \
.filter(F.date_trunc('dd', df.dropOff_datetime) <= F.lit("2019-10-31")) \
.filter(df.dropOff_datetime > df.pickup_datetime) \
.withColumn("unix_pickup_datetime", F.unix_timestamp(df.pickup_datetime)) \
.withColumn("unix_dropoff_datetime", F.unix_timestamp(df.dropOff_datetime)) \
.withColumn("seconds_between", F.col("unix_dropoff_datetime") - F.col("unix_pickup_datetime")) \
.withColumn("minutes_between", F.col("seconds_between").cast("bigint")/60) \
.withColumn("hours_between", F.col("minutes_between").cast("bigint")/60) \
.select('pickup_datetime', 'dropoff_datetime', "minutes_between", "hours_between") \
.sort("hours_between", ascending = False) \
.show()

## Q4. Spark’s User Interface which shows the application's dashboard runs on which local port?
spark
# change docker containerID to localhost in IP address

## Q6.Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?
#download tzxi zone file locally
os.system('curl -O https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv')

# read a csv file into the spark session
df1 = spark.read \
  .option("header", "true") \
  .csv('taxi+_zone_lookup.csv')

# verify zone data downloaded successfully
df1.show()

# method1 sql spark
df1.createOrReplaceTempView('taxi_zone')

spark.sql(""" select z.Zone, count(dispatching_base_num)
from fhv_trip_data fhv
join taxi_zone z on fhv.PUlocationID = z.LocationID
group by z.Zone
order by 2
""").show()

# method2 pyspark filtering and sorting
df \
.join(df1.withColumnRenamed('LocationID', 'PUlocationID'), on = ['PUlocationID'], how = 'left') \
.groupBy('Zone') \
.count() \
.sort("count") \
.show()

# close connection when done with session
spark.stop()
