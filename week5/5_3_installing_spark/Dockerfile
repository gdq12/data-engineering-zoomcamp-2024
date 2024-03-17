FROM spark:3.5.1-scala2.12-java11-python3-ubuntu

# for non root users so can pip install
# based on this post: https://stackoverflow.com/questions/71753536/how-to-deal-with-permission-errors-with-pip-inside-a-docker-compose-container
USER root
ARG USERNAME=ubuntu
RUN adduser --uid 1000 --disabled-password ${USERNAME}
USER ${USERNAME}
ENV PATH="$PATH:/home/${USERNAME}/.local/bin"

# final working directory
WORKDIR /home/ubuntu
EXPOSE 8501

# pip install all other libraries
COPY . /home/ubuntu/
RUN cd /home/ubuntu && \
    pip install --no-cache-dir -r requirements.txt

# command to run when container launched
CMD ["bash"]
