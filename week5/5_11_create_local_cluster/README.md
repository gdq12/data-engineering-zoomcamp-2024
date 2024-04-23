### Working with Spark standalone cluster in jupyter notebook

1) initiate docker container `docker run -it -p 8888:8888 -p 8080:8080 -e ROOT=TRUE wk5-spark`

  + port `8888` is used to access jupyter lab UI

  + port `4040` is used to access spark local cluster UI

  + port `8080` is used to access the spark stand alone cluster UI

2) initiate jupyter notebook:

    ```{bash}
    jupyter-lab --generate-config
    # will be prompted to create a password
    jupyter-lab password

    # follwoing will prompt a series of Qs, only need to answer the first and the rest can leave blank
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem

    # move needed file for jupyter-lab connection
    mv /home/ubuntu/jupyter_server_config.py /home/ubuntu/.jupyter
    ```
3) initiate jupyter-lab from wihtin the container:

    ```{bash}
    # initiate jupyter-lab in docker
    jupyter-lab --ip 0.0.0.0 --port 8888 --no-browser --allow-root
    # opening jupyter lab in the browser
    http://127.0.0.1:8888/lab
    ```

4) run python script:

  ``` {python}
  import os
  import pyspark
  from pyspark.sql import SparkSession
  from datetime import date
  import datetime as datetime
  from dateutil.relativedelta import relativedelta
  from pyspark.sql import functions as F

  # start spark stand alone cluster
  ## find out where spark is installed
  os.environ['SPARK_HOME']
  ## start the master cluster
  os.system(f"{os.environ['SPARK_HOME']}/sbin/start-master.sh")
  ## start worker
  os.system(f"{os.environ['SPARK_HOME']}/sbin/start-worker.sh spark://{os.environ['HOSTNAME']}:7077")

  # connect to a spark standalone cluster (get the cluster path from spark UI URL value)
  spark = SparkSession.builder \
      .master(f"spark://{os.environ['HOSTNAME']}:7077") \
      .appName('test') \
      .getOrCreate()

  # check working with the stand alone cluster
  spark

  # create sub folder to download parquets into
  os.system('mkdir grn_taxi_data')
  os.system('mkdir yellow_taxi_data')

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
  df_grn_sel.createOrReplaceTempView('grn_data')
  df_yellow_sel.createOrReplaceTempView('yellow_data')

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

  # export it to another parquet file
  df_join.write.parquet('summary_stats/total', mode = 'overwrite')

  # stop spark session
  spark.stop()

  # stop spark stand alone cluster and worker
  os.system(f"{os.environ['SPARK_HOME']}/sbin/stop-master.sh")
  os.system(f"{os.environ['SPARK_HOME']}/sbin/stop-worker.sh spark://{os.environ['HOSTNAME']}:7077")
  ```

5) convert notebook to `.py` file/script: `jupyter nbconvert --to=script vid11_wk5.ipynb` --> also clean it up if needed

6) execute python script in command line: `python3 vid11_wk5.py`

7) the code above is updated so inputs can be provided from the command line:

  ``` {bash}
  URL=spark://$HOSTNAME:7077

  /home/ubuntu/spark-3.5.1-bin-hadoop3/bin/spark-submit \
    --master="${URL}" \
      vid11_wk5.py \
      --input_start_date=2020-01-01\
      --input_end_date=2021-12-31
  ```

  + provides input arguments to use specific start and end dates for NYC taxi data URL parsing

  + it can also pass the URL of the spark stand alone cluster via `spark-submit`

### Helpful links

* YT [video](https://www.youtube.com/watch?v=HXBwSlXo5IA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=65)

* Spark standalone mode [documentation](https://spark.apache.org/docs/latest/spark-standalone.html)
