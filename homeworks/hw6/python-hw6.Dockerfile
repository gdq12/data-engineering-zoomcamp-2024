# Reference from offical Apache Spark repository Dockerfile for Kubernetes
# https://github.com/apache/spark/blob/master/resource-managers/kubernetes/docker/src/main/dockerfiles/spark/Dockerfile
ARG java_image_tag=17-jre
FROM eclipse-temurin:${java_image_tag}

# -- Layer: OS + Python

ARG shared_workspace=/opt/workspace

RUN mkdir -p ${shared_workspace} && \
    apt-get update -y && \
    apt-get install -y python3 && \
    ln -s /usr/bin/python3 /usr/bin/python 

ARG spark_version=3.3.1
ARG jupyterlab_version=3.6.1

RUN apt-get install -y python3-venv python3-pip 

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install wget pyspark==${spark_version} jupyterlab==${jupyterlab_version}

ENV PATH="/opt/venv/bin:$PATH"

ENV SHARED_WORKSPACE=${shared_workspace}

# -- Runtime
EXPOSE 8888
WORKDIR /home/ubuntu
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=