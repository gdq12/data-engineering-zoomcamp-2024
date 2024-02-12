### Background 

This is a Mage "learning" sub repo. It is used to follow tutorials provided in week 2 of [DE zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration). This page provides organized documentation on the learned file structure and how to's of this tool.

### Config Files

I. [io_config.yaml](./magic-zoomcamp/io_config.yaml)

* defined variable credentials per profile. This is where testing and dev profiles can be defined 

* when initiating the docker image, the credentials definitions that are saved in the `.env` file are captured (interpolating) into this file via jinja syntax: `{{ env_var('var_name') }}`

* credential to connect to cloud services are also defined here. Once they have been created and downloaded locally to the target location. The following can be done: 

    - add a copy command to `Dockerfile` so it can be copied into a mage container once its up and running: `COPY *secrets*.json ${USER_CODE_PATH}/*secrets*.json` (perhaps this is over kill, just having it mounted to the image upon docker run/compose should be sufficient)

    - have it mounted to the target directory in the container via `docker-compose.yml`: `./*secrets*.json:/home/src/` 

    - update `io_config.yaml` so that instead of defining all of the json vars individually, it can be just read straight from the json file via env var `GOOGLE_SERVICE_ACC_KEY_FILEPATH`. Also verify that `GOOGLE_LOCATION` has the correct region. 

### Pipeline Setup 

- the setup info and files executed when a pipeline is triggered reside in different folders in the project directory 

- pipeline configuration info 

    * this resides in `pipelines/pipelineName/metadata.yaml`

    * it lists all the blocks within the pipeline that are created/executed in sequential order

    * it consists of necessary info like which script is upstream/downstream of the script of intrest, what language has the script been written in, the block name, its execution status, type of script (data_exporters, data_loaders, etc.) etc.

    * at the end of this yaml file it states higher level info of the pipeline: variable definition location, when it was created, types etc. 

- the scripts are of the actual pipeline are location in the block subfolders (data_exporters, data_loaders, transformers). These subfolders will prob consists of blocks from multiple pipelines, but the pipeline organization and to which pipeline they pertain to can also be derived from `pipelines/pipelineName/metadata.yaml`.

    * the advantage of this is that it is wasier to use pipeline blocks across multiple pipeline without having to duplicate code 

    * when using blocks from other pipeline for another, can essentially drag and drop the blocks from the file window to the open pipeline window. can use the GUI to then form a sequential link between them, this should be updated in the pipelines `metadata.yaml` file

- triggers can be setup to schedule pipeline executions, have them run parallel or trigger each other etc. at the moment, the UI didnt create a file in the repo once a trigger schedule was created, but there is documentation how these triggers can be setup with code. It can be found [here](https://docs.mage.ai/orchestration/triggers/configure-triggers-in-code)

### Variable setups 

- defualt variables can be accessed in a pipeline script via `kwargs`. The set default can either be viewed by executing `print(kwargs)` or looking at the listed one in the documentation [here](https://docs.mage.ai/getting-started/runtime-variable#using-runtime-variables)

- new variables can be created for pipelines and triggers in the GUI in respective pipelines by going to the `variables`/`Runtime variables` option in the left panel 

- custom variable definition are saved in the pipelines `metadata.yaml` file. To customize them via code instead of the GUI, best to follow this [documentation](https://docs.mage.ai/getting-started/runtime-variable#using-runtime-variables)

- further documentation: [runtime variables](https://docs.mage.ai/getting-started/runtime-variable) and [variables in Mage](https://docs.mage.ai/development/variables/overview)

### Backfills

- its like going back in time and collecting possible missing data 

- if data collection is based on an execution date, then its like creating a for loop to fetch info from that execution date 

- caution this is dependent on the pipeline using `kwargs['execution_date']` in the pipeline scripts 

- this can be set up in the UI, as explained [here](https://docs.mage.ai/orchestration/backfills/guides)

- it seems that no code files are created for this, but apart from using the UI, one can make API calls to execute this. documentation on this is found [here](https://docs.mage.ai/api-reference/backfills/overview)