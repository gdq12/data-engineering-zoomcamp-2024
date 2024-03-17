### Working with Docker Spark

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

### Helpful Links

* Guidelines for local [installations](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/05-batch/setup)

* YT [video](https://www.youtube.com/watch?v=hqUbB9c8sKg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=54)

* apache spark [docker images tags](https://hub.docker.com/_/spark/tags?page=1)
