FROM python:3.10

WORKDIR /home/ubuntu/

# pip install all other libraries
COPY requirements.txt /home/ubuntu/
RUN pip install -r requirements.txt

# command to run when container launched
CMD ["bash"]