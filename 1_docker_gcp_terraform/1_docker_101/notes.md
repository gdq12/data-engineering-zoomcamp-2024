### I. Why Docker

- containerization technology that allows a user to create an isolated ETL pipeline for instance that is independent of global environment/configurations
- in collaborative work, can develop apps/projects that should work in all systems (linux/apple/windows/cloud etc.)
- no need to install programs/DWH into host machine, will sit in the container only
- permit reproducibility
- it permits more controlled tests and verify of anticipated results (ex. CI/CD)
- it is meant to be as independent from the host env as possible and be able to run with efficiency in any system regardless of system architecture.

### II. Creating a Docker Image

- when enter and then exit a container, all work/installations done will be erased, so better create a Dockerfile to auto install the correct configurations when creating a container.

- example **Dockerfile**

```
# image to pull form docker repo
FROM python:3.9

# define the working directory and CD there
WORKDIR /app

# install python libraries needed
RUN pip install pandas
RUN pip install pyarrow

# copy all files from local to container
COPY . /app

# copy scripts form local machine to image
COPY pipeline1.py /app

# command to run once the container starts running
ENTRYPOINT ["python", "pipeline1.py"]
```

### III. Breakdown of Docker commands

* pulling an image from docker hub and building a container from it

  ``` {bash}
  docker run -it --entrypoint=bash python:3.9
  ```
  * run: to build or relaunch a container based on an image
  * -it: to run a container in interactive mode, reactive to commands carries out in terminal
  * python: name of image
  * --entrypoint=bash: the command to be executed in the container once launched
  * :3.9: its a tag of the image. images can be version controlled, so tags are typically versions.

* building a docker image from the local Dockerfile

  ```{bash}
  docker build -t test:1.1 .
  ```
  * build: it build an image from a configuration file (it always has to be Dockerfile)
  * -t: means to tag an image, it is mandatory to always use this
  * test:1.1: name and tag of the image
  * ".": to build the image based on the Dockerfile in the current directory

### IV. Python pipeline script


```{python}
import sys
import pandas as pd

# sys.argv are command line arguments passed to the script
print(sys.argv)

# 0 is the name of the file, 1 is whatever is passed from command line
print(sys.argv[0])

day = sys.argv[1]

print(f'job complete on {day}, good job!')
```

* here sys.argv takes arguments from the scripts local environment for script run use. The argument can be passed on to a docker running container via the docker run command:

  ```{bash}
  docker run -it test:pd 2024-01-24
  ```
  * 2024-01-24: argument to pass on to script that is executed when the container starts to run.

### Helpful Links

* Youtube video of [lesson](https://www.youtube.com/watch?v=EYNwNlOrpr0&t=1435s)

* lecturer's [notes](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)
