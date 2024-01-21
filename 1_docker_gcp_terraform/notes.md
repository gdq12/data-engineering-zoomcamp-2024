1. Docker

  - main features are containers and isolation. great for data pipelines.

  - it is meant to be as independent from the host env as possible and be able to run with efficiency in any system regardless of system architecture.

  - docker command break down

    ``` {bash}
    docker run -it --entrypoint=bash python:3.9
    ```
    * run: to build or relaunch a container based on an image
    * -it: to run a container in interactive mode, reactive to commands carries out in terminal
    * python: name of image
    * --entrypoint=bash: the command to be executed in the container once launched
    * :3.9: its a tag of the image. images can be version controlled, so tags are typically versions.

    ```{bash}
    docker build -t test:1.1 .
    ```
    * build: it build an image from a configuration file (it always has to be Dockerfile)
    * -t: means to tag an image, it is mandatory to always use this
    * test:1.1: name and tag of the image
    * ".": to build the image based on the Dockerfile in the current directory
    ```{bash}
    docker run -it test:pd 2024-01-24
    ```
    * 2024-01-24: argument to pass on to script that is executed when the container starts to run.

    
