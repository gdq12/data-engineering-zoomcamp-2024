FROM python:3.9.1
    
RUN pip install pandas pyarrow fastparquet sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py

# need to use entrypoint rather than CMD so argparse arguments can be passed in docker run command
# ENTRYPOINT ["python", "ingest_data.py"]
ENTRYPOINT ["bash"]