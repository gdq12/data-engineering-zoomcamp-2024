### Connecting to GCP w/Jupyter Notebook

1) Initiate jupyter notebook  

* updated the docker image to include

* enter the docker container: `docker run -it -p 8888:8888 -e ROOT=TRUE week5_spark`

* execute the following to create ssh connex btw local PC and docker container

    ```{bash}
    jupyter-lab --generate-config
    # will be prompted to create a password
    jupyter-lab password

    # follwoing will prompt a series of Qs, only need to answer the first and the rest can leave blank
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem

    # move needed file for jupyter-lab connection
    mv /home/ubuntu/jupyter_server_config.py /home/ubuntu/.jupyter
    ```

* initiate jupyter-lab from wihtin the container:

    ```{bash}
    # initiate jupyter-lab in docker
    jupyter-lab --ip 0.0.0.0 --port 8888 --no-browser --allow-root
    # opening jupyter lab in the browser
    http://127.0.0.1:8888/lab
    ```

### Spark and GCP

1) Create a new bucket in GCP `spark-wk5-tutorial` with multi-region being in the EU, all other settings left at default with disabling data recovery option

2) execute following python script to work with Spark and GCP

``` {python}
# import needed libraries
import os
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
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

# close session to create a new conex later
spark.stop()

# authenticate connex to cloud storage
!gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

# copy parquets to cloud storage
!gsutil -m cp -r /home/ubuntu/grn_taxi_data/*.parquet gs://spark-wk5-tutorial/grn_taxi_data/
!gsutil -m cp -r /home/ubuntu/yellow_taxi_data/*.parquet gs://spark-wk5-tutorial/yellow_taxi_data/

# remove parquets locally to make sure pull from gcp worked
!rm -r /home/ubuntu/grn_taxi_data
!rm -r /home/ubuntu/yellow_taxi_data

# reconnect to spark with the adjusted configuration
credentials_location = '/home/ubuntu/ny-taxi-412905-ac957361bbc4.json'

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "/home/ubuntu/gcs-connector-hadoop3-latest.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)

# create spark context: this converts the gs address of the cloud storage to a com.google path using the hadoop jar file  
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

# connect to a spark session
spark = SparkSession.builder \
  .master("local[*]") \
  .appName('test') \
  .getOrCreate()

# read in the file to spark
df_grn = spark.read.parquet('gs://spark-wk5-tutorial/grn_taxi_data/*')

df_yellow = spark.read.parquet('gs://spark-wk5-tutorial/yellow_taxi_data/*')

# verify the parquets were fetched from cloud storage
df_grn.show()
df_grn.count()

df_yellow.show()
df_yellow.count()

# close session to create a new conex later
spark.stop()
```

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=Yyz293hBVcQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=64)
