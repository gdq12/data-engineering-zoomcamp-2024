### Starting a dbt project 

1. Create something that resembles a repository where the project will be stored 

    - can opt to use dbt's starter project [repo](https://github.com/dbt-labs/dbt-starter-project)

        * provides folders/files needed including sample models 

    - important files needed: 

        - `profile.yml`: define global settings for the project, profile (which DB wil be using to run project)

2. getting the starter project started 

    - can be done locally by running `dbt init` in the directory when want to host the project 

    - via dbt cloud (more UI based)

3. set up schemas/tables in big query 

    - there should be types 3 schema: raw, transform, production

    - dbt expects for the raw data to already be placed in the raw centric schema 

    - dbts main work is in the transformation schema 

    - dbt aim to have production ready tables in the production schema 

### Setting up dbt with Bigquery 

1. create a free develope dbt cloud account, based on instructions found [here](https://www.getdbt.com/signup)

    * an account will be created based on what organization is stated during the registration 

2. create a service account in Bigquery 

    - go to Bigquery [credential wizerd]
(https://console.cloud.google.com/apis/credentials/wizard?project=ny-taxi-412905)

    - select the following:

        * select an API: `BigQuery API`

        * what data will you be acessing: `Application data`

        * click continue in the popup window

        * assign a service account name: `dbt-service-account`

        * role: `BigQuery Admin`

        * in the credential page --> click on service account that just created 

        * select keys tab 

        * `add key` --> `create new key` --> `json` format

        * json will be auto-downloaded to PC

4. create a new project in dbt Cloud [here](https://cloud.getdbt.com/) 

    * top right corner go to settings next to account name 

        * click projects in the left panel 

        * click on `+ New Project`

    * name project `4_3_start_w_dbt`

    * choose connection: `BigQuery`

    * upload service account json file produced from step2

    * dataset/schema name dbt will set up during trasnformations: `transform_wk4_v1`

    * `test connection`

5. add git repo to project 

    * in the settings to setup repo for project --> select git clone and paste repo SSH into the box

    * copy the key string and paste it in: github repo setting --> deploy keys --> `add new` --> `allow write access` --> `add key`

6. `Start developing in the IDE`: click on this option when the "Your project is ready window appears"

    - this step clones the repo to the remote IDE

    - offers to provide a brief tour, best to do to more easily navigate throughout the rest of the tutorial 

### Setting up project in dbt Cloud (all carried out in dbt CLoud IDE)

1. create new branch: `dbt-cloud-wk4-lesson3`

2. in the left panel click on `initialize dbt project`. It will create a sereies of folders and file in the principle file path of the repo but this can be moved after the pull request 
    
    - adds the following to `.gitignore`: `target/`, `dbt_packages/`, `logs/`

    - adds the following folders: `tests`, `analyses`, `models`, `macros`, `seeds`, `snapshots`

    - add the following file: `dbt_profile.yml`

3. good to know for the `dbt_profile.yml`

    - its a file that defines a project and paths where most needed config files are to be found 

    - can determine things like what profile dbt should run under, what type od table models dbt should be creating etc

### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1xSll_jv0T8JF4rYZvLHfkJXYqUjPtThA/edit#slide=id.p1)

* Lesson YT [video](https://www.youtube.com/watch?v=iMxh6s_wL4Q&t=1s)

* week4 [repo page](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/04-analytics-engineering)

* dbt [documnetation page](https://docs.getdbt.com/docs/introduction)

* Links for helping set up DBT:

    - Github [page](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/dbt_cloud_setup.md) to set up dbt Cloud with Bigquery 

    - Github [dbt-core with BigQuery setup](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/docker_setup/README.md) (if not interested in using dbt Cloud)



