# image to pull form docker repo
FROM python:3.9

# define the working directory and CD there
WORKDIR /app

# install python libraries needed
RUN pip install pandas
RUN pip install pyarrow

# copy scripts form local machine to image
COPY pipeline1.py /app

# command to run once the container starts running
ENTRYPOINT ["python", "pipeline1.py"]
