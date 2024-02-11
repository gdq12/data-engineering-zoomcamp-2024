### Background 

This is a Mage "learning" sub repo. It is used to follow tutorials provided in week 2 of [DE zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration). This page provides organized documentation on the learned file structure and how to's of this tool.

### Config Files

I. [io_config.yaml](./magic-zoomcamp/io_config.yaml)

* defined variable credentials per profile. This is where testing and dev profiles can be defined 

* when initiating the docker image, the credentials definitions that are saved in the `.env` file are captured (interpolating) into this file via jinja syntax: `{{ env_var('var_name') }}`

### Pipeline Setup 

- the setup info and files executed when a pipeline is triggered reside in different folders in the project directory 

- pipeline configuration info 

    * this resides in `pipelines/pipelineName/metadata.yaml`

    * it lists all the blocks within the pipeline that are created/executed in sequential order

    * it consists of necessary info like which script is upstream/downstream of the script of intrest, what language has the script been written in, the block name, its execution status, type of script (data_exporters, data_loaders, etc.) etc.

    * at the end of this yaml file it states higher level info of the pipeline: variable definition location, when it was created, types etc. 

- the scripts are of the actual pipeline are location in the block subfolders (data_exporters, data_loaders, transformers). These subfolders will prob consists of blocks from multiple pipelines, but the pipeline rganization and to which pipeline they pertain to can also be derived from `pipelines/pipelineName/metadata.yaml`.