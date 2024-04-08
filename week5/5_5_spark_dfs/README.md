### Code used during session

``` {python}
# import needed libraries
import os
import pyspark
from pyspark.sql import SparkSession

# connect to a spark session
spark = SparkSession.builder \
  .master("local[*]") \
  .appName('test') \
  .getOrCreate()

# download file locally
os.system('curl -O https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2021-01.parquet')

# read in the file to python
df = spark.read \
    .option("header", "true") \
    .parquet('fhvhv_tripdata_2021-01.parquet')

# inspecting the df a bit
df.schema
df.printSchema()

# selecting and filtering the DF
df.select('pickup_datetime', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
    .filter(df.hvfhs_license_num == 'HV0003') \
    .show()

# other functions available in spark
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# adding new columns to DF
df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .select('pickup_date', 'pickup_datetime', 'dropoff_date', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
    .show()

# creating a custom function in spark
def crazy_stuff(base_num):
    num = int(base_num[1:])
    if num % 7 == 0:
        return f's/{num:03x}'
    else:
        return f'e/{num:03x}'

crazy_stuff_udf = F.udf(crazy_stuff, returnType = StringType())

# apply custom function to DF
df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .select(crazy_stuff_udf(df.dispatching_base_num).alias('base_id'), 'pickup_date', 'pickup_datetime', 'dropoff_date', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
    .show()
```

### Types of Spark commands

* there are some commands that are executed right away while some are "lazy" commands which arent executed right away but instead are saved in a queue of commands that are only executed when coupled with those non-lazy commands

* actions vs transformations: actions are commands that are executed right away (eager), transformations are "lazy" commands that arent executed right away

* transformation commands:

  - select columns

  - filtering rows

  - joins

  - groupby

  - withColumn() (adds a new Col to DF)

* action commands:

  - show()

  - take()

  - head()

  - write

### To note

When using udf (user defined functions), couldnt use them with withColumn() function. Ideally it would of been better to create a new column using the following syntax:

``` {python}
df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .withColumn('base_id', crazy_stuff_udf(df.dispatching_base_num)) \
    .select('base_id', 'pickup_date', 'pickup_datetime', 'dropoff_date', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
    .show()
```

But an unknown parsing error occurred, so instead the column transformation occurred in the select function as follows:

``` {python}
df \
    .withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .withColumn('dropoff_date', F.to_date(df.dropoff_datetime)) \
    .select(crazy_stuff_udf(df.dispatching_base_num).alias('base_id'), 'pickup_date', 'pickup_datetime', 'dropoff_date', 'dropoff_datetime', 'PULocationID', 'DOLocationID') \
    .show()
```
  
### Helpful Links

* YT [lesson](https://www.youtube.com/watch?v=ti3aC1m3rE8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=56)
