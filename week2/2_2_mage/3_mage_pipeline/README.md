### I. Starting Mage

```{bash}
# going to target directory 
cd ~/git_repos/data-engineering-zoomcamp-2024/2_mage_repo

# build the container from Dockerfile
docker compose build 

# get everything up and running 
docker compose up 
```

### II. Exploring the GUI

- Go to http://localhost:6789/

- In edit pipeline (in left panel bar), its an interactive way to view the files that are used for building/running/facilitating the pipeline

- GUI has an interactive diagram that shows how the pipelines work with each other: show what objects from the previous one are used in the consecutive one.

- Can execute the full pipeline by visiting the last block and clicking the triple dots on the right hand corner of the screen to execute 

### Good to knows about the set

- defining project 

    * this is defined by `PROJECT_NAME` in the `.env` file which is then used to establish a directory of the same name in the local system and within the running mage docker container

- .gitignore 

    * the default `.gitignore` in the tutorial has all the files/directories from the `docker compose up` non-commited. The lines that are actually specific to this can be found in this [.gitignore](../../.gitignore)


### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=stI-gg4QBnI&t=1s)