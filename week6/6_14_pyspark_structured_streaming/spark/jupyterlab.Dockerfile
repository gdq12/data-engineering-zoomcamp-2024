FROM cluster-base

# -- Layer: JupyterLab
ARG spark_version=3.3.1
ARG jupyterlab_version=3.6.1

### Added ####
# Install required dependencies
RUN apt-get update -y && \
    apt-get install -y python3-venv python3-pip

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment and install required packages
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install wget pyspark==${spark_version} jupyterlab==${jupyterlab_version}

# Set the PATH to use the virtual environment's Python and pip
ENV PATH="/opt/venv/bin:$PATH"
##### Removed ###
# RUN apt-get update -y && \
#     apt-get install -y python3-pip python3-venv && \
#     pip3 install wget pyspark==${spark_version} jupyterlab==${jupyterlab_version}
###

# -- Runtime
EXPOSE 8888
WORKDIR /home/ubuntu
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=