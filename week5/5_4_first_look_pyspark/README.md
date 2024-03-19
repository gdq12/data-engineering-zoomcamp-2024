### Code used during session

```{python}
# import needed libraries
import os
import pyspark
from pyspark.sql import SparkSession

# connect to a spark session
spark = SparkSession.builder \
  .master("local[*]") \
  .appName('test') \
  .getOrCreate()

# read in the file to python
df = spark.read \
    .option("header", "true") \
    .csv('fhvhv_tripdata_2021-01.csv')

# to verify that the header were correctly detected
df.show()

# row by row print out of df
df.head(5)

# summary of what columns and data types were imported
df.schema

# use pandas to infer data types

# partition the data a bit so can use it with pandas
!head -n 1001 fhvhv_tripdata_2021-01.csv > head.csv
import pandas as pd
df_head = pd.read_csv('head.csv')

# verify that pandas worked
df_head.head()

# get the data types
df_head.dtypes

# use spark to convert a pandas df to spark df
spark.createDataFrame(df_head).show()
spark.createDataFrame(df_head).schema

# convert pyspark data types
from pyspark.sql import types

# mix of python and scala syntax: list and types. is python, everything else is scala
schema = types.StructType([
  types.StructField('hvfhs_license_num', types.StringType(), True),
  types.StructField('dispatching_base_num', types.StringType(), True),
  types.StructField('pickup_datetime', types.TimestampType(), True),
  types.StructField('dropoff_datetime', types.TimestampType(), True),
  types.StructField('PULocationID', types.IntegerType(), True),
  types.StructField('DOLocationID', types.IntegerType(), True),
  types.StructField('SR_Flag', types.IntegerType(), True)
])

# reimport data with correct data types
df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv('fhvhv_tripdata_2021-01.csv')

# inspeact to make sure the data type application change is correct
df.show()
df.schema
df.head(10)

# to repartition a large file and save locally
df = df.repartition(24)
# save the parquets for the first time
df.write.parquet('fhvhv/2021/01/')
# to overwrite it without creating a new directory
df.write.parquet('fhvhv/2021/01/', mode = 'overwrite')
```

### Internals of Spark

* for a given spark cluster, there are a series of executers (aka computers) that conduct computational work

* for a given file in a remote storage (GC for example) it will be linked/assigned to a single executor --> once the executor is done processing the file, it will move on to the next file that isn't currently linked to an executor at the time

* if there is only 1 very large file available this limits the computing capacity of spark (only 1 executor is occupied and the rest remain idle) --> so this is the reason why the file should be split into smaller ones so all the executor can be occupied and the process can finish faster

### Good to knows throughout session

* can visit spark UI by going to `localhost:4040` (can visit once have port forwarding configured correctly)

* the course recording was done when csv files were still made available on the nyc taxi dataset website. Since this was no longer available, downloaded the data from the courses github repo [page](https://github.com/DataTalksClub/nyc-tlc-data/) and then docker copied it over

* able to actually import parquets from links by changing the following:

  ```{python}
  df = spark.read \
      .option("header", "true") \
      .parquet('fhvhv_tripdata_2021-01.parquet')
  ```

  - when looking into the df via `df.show()`, `df.head(5)` and `df.schema` see that the parquet files already come with the correct data type

* good to knows about pyspark behavior

  - unlike pandas, pyspark doens't infer data types, all columns are auto read as strings

  - best to try to save the optimal data types: integer takes 4 bytes while longtype/string takes up 8 bytes

  - in order to change data types pyspark, must pass scala syntax into a function

  - `df.repartition` is a lazy command, doesn't really execute anything (as seen in spark UI) --> it simply defines what will be executed in the future. It wont be executed until something is done with the data like saving it to a remote/local location

    + repartitioning is an expensive operation so it may take some time

    + while data is being saved to parquets, print statements give an idea as to what is going on: `Stage8:===================> (0 + 4) / 6]`

      - 6: number of partitions pyspark auto split the large file into and that currently working with to repartition

      - 4: the number of executors that pyspark has allocated for this, default value defined from the start session `spark = SparkSession.builder.master("local[*]").appName('test').getOrCreate()`

      - Stage8: the job ID it was assigned, can use this as reference to see the progress in spark UI

    + once the writing of the files are complete, know that the files were completely saved when in the target subdirectory it was saved in see an empty file called `_SUCCESS`. When this file is absent, it is an indication that something went wrong

    + spark refuses to overwrite by default

### Helpful Links

* YT [lesson](https://www.youtube.com/watch?v=r_Sf6fCB40c&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=55)
