FROM python:3.10

# final working directory
WORKDIR /home/ubuntu/
EXPOSE 8501
# ENV HOME="/home/ubuntu"
#
# install java
RUN wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz && \
  tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz && \
  rm openjdk-11.0.2_linux-x64_bin.tar.gz

ENV JAVA_HOME="${HOME}/jdk-11.0.2"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# installing Spark
RUN wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz && \
  tar xzfv spark-3.3.2-bin-hadoop3.tgz && \
  rm spark-3.3.2-bin-hadoop3.tgz

ENV SPARK_HOME="${HOME}/spark-3.3.2-bin-hadoop3"
ENV PATH="${SPARK_HOME}/bin:${PATH}"

# pip install all other libraries
COPY . /home/ubuntu/
RUN cd /home/ubuntu && \
    pip install --no-cache-dir -r requirements.txt

# vars for pyspark
ENV PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"

# command to run when container launched
CMD ["bash"]

# docker buid command
# docker build -t wk5-spark:latest .
# docker run command
# docker run -t wk5-spark:latest
