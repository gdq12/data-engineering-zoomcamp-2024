### Testing out Docker Image from Spark

* attempted the official docker image to work with spark in a controlled env

1. pull the docker image from docker hub

  ```{bash}
  docker pull spark:3.5.1-scala2.12-java11-python3-ubuntu
  ```

2. testing out docker spark

  ```{bash}
  # start scala shell
  docker run -it spark:3.5.1-scala2.12-java11-python3-ubuntu /opt/spark/bin/spark-shell

  # tesint out scala commands
  val data = 1 to 10000
  val distData = sc.parallelize(data)
  distData.filter(_ < 10).collect()

  # other command to test out
  spark.range(1000 * 1000 * 1000).count()
  ```

### Working with Pyspark

* chose to go with a docker image pre-made by spark to deal with different PCs architectures and installations.

* had to use that as a layer to build a custom image in order to create ouwn user and pip install python libraries

* running pyspark in jupyter notebook

  ```{python}
  # needed libraries
  import os
  import pyspark
  from pyspark.sql import SparkSession

  # to check what version have installed
  pyspark.__version__

  # check path of where it was pip installed
  pyspark.__file__

  #download tzxi zone file locally
  os.system('curl -O https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv')

  # connect to a spark session
  spark = SparkSession.builder \
      .master("local[4]") \
      .appName('test') \
      .getOrCreate()


  # read a csv file into the spark session
  df = spark.read \
      .option("header", "true") \
      .csv('taxi+_zone_lookup.csv')

  # prints out the first 20 rows
  df.show()

  # saves parquet files locally
  df.write.parquet('zones')
  ```

  - good to knows:

    + `.master("local[4]")`: for a given spark session it indicated how many CPUs should be allocated for that builder

    + via `localhost:4040` can visit spark UI to see how the clusters are doing. Can add this port to port forwarding when working in VScode

    + by default spark doesnt know what the file header is, this can be done by indicating the column row with the following `.option("header", "true")`

### Issues with PC

* currently have issues initiating vs code extensions in dev container on mac intel based chip only, not the case for an m2 chip --> cant use jupyter notebook without the extension in vs code

* blogs to look into to resolve this:

  - https://github.com/microsoft/vscode-remote-release/issues/8967

  - https://code.visualstudio.com/remote/advancedcontainers/change-default-source-mount

* in the meantime, using the same method as described in [week4/4_1a_data_2_gcs](../week4/4_1a_data_2_gcs:

  * enter the docker container: `docker run -it -p 8888:8888 -e ROOT=TRUE wk5-spark`

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

### Helpful Links

* Guidelines for local [installations](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/05-batch/setup)

* YT [video](https://www.youtube.com/watch?v=hqUbB9c8sKg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=54)

* apache spark [docker images tags](https://hub.docker.com/_/spark/tags?page=1)

* apache spark docker [github page](https://github.com/apache/spark-docker/blob/master/OVERVIEW.md#environment-variable)
