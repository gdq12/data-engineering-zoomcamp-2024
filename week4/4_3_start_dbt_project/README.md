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

2. Connect Bigquery to dbt Cloud. dbt offers [documentation](https://docs.getdbt.com/guides/bigquery?step=1) but there is also a course [README](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/dbt_cloud_setup.md)

3. create a service account in Bigquery 

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

    * either have to create a new project or will be on a page where asked to complete project setup

    * name project `de-zoomcamp-wk3`

    * choose connection: `BigQuery`

    * upload service account json file produced in step 3

    * accept all --> verify dataset name is `nytaxi_wk3_dbt`

    * `test connection`

5. add git repo to project 

    * in the settings to setup repo for project --> select git clone and paste repo SSH into the box

    * copy the key string and paste it in: github repo setting --> deploy keys --> `add new` --> `allow write access` --> `add key`

6. install dbt Cloud CLI, based on these [instructions](https://cloud.getdbt.com/settings/profile/cloud-cli), this step didnt work, will try to fix it later 

    * installing commands 
    
        ```{bash}
        # using brew (for global installation)
        brew untap dbt-labs/dbt 
        brew tap dbt-labs/dbt-cli 
        brew install dbt

        # using python (should do within a docker)
        pip3 install dbt --no-cache-dir
        ```

    * add configuration file to PC 

        ```{bash}
        mkdir ~/.dbt
        mv ~/Downloads/dbt_cloud.yml ~/.dbt/.
        ```


### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1xSll_jv0T8JF4rYZvLHfkJXYqUjPtThA/edit#slide=id.p1)

* Github [page](https://github.com/DataTalksClub/nyc-tlc-data/) for data needed for dbt project 

* Github [dbt-cloud setup](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/dbt_cloud_setup.md)

* Github [dbt-core with BigQuery setup](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/docker_setup/README.md)

* dbt [documnetation page](https://docs.getdbt.com/docs/introduction)

* Lesson YT [video](https://www.youtube.com/watch?v=iMxh6s_wL4Q&t=1s)