FROM python:3.12

WORKDIR /home/ubuntu
EXPOSE 8888

# make sure working with the latest ubuntu configs
RUN apt-get update && \
    apt-get clean

# copy needed files needed for creating python container 
COPY requirements.txt /home/ubuntu
RUN pip install -r requirements.txt 

# command to run when container is up and running 
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=
