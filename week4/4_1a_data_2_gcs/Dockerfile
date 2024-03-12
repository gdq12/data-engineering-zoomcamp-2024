FROM python:3.10

WORKDIR /home/ubuntu/
EXPOSE 8501

# pip install all other libraries
COPY . /home/ubuntu/
RUN pip install -r requirements.txt

# command to run when container launched
CMD ["bash"]
