### Starting a dbt project

1. In Bigquery, create the needed schemas and copy over the raw data from gcs. This is done using [gcs_2_bigquery.sql](../4_1a_data_2_gcs/gcs_2_bigquery.sql). This creates the following:

    - dataset/datawarehouse: `ny-taxi-412905`

    - schemas:

        + `nytaxi_wk4_dbt_raw`

            - tbls:

                + `external_green_trip_data`

                + `external_yellow_trip_data`

                + `external_fhv_trip_data`

        + `nytaxi_wk4_dbt_transform`

        + `nytaxi_wk4_dbt_prod`

2. other (not sure where this goes)

    a. Create something that resembles a repository where the project will be stored

        - can opt to use dbt's starter project [repo](https://github.com/dbt-labs/dbt-starter-project)

            * provides folders/files needed including sample models

        - important files needed:

            - `profile.yml`: define global settings for the project, profile (which DB wil be using to run project)

    b. getting the starter project started

        - can be done locally by running `dbt init` in the directory when want to host the project

        - via dbt cloud (more UI based)

    c. set up schemas/tables in big query

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

        * define a subdirectory so file system only created in a specific part of the repo: `4_3_dbt_cloud`

    * choose connection: `BigQuery`

    * upload service account json file produced from step2

        - specify location so queries run only under a specific location: `europe-west1`

    * dataset/schema name dbt will set up during trasnformations: `nytaxi_wk4_dbt_transform`

        - this schema should be created in Bigquery before starting to model in dbt (this was already created in Bigquery)

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

    - all of these files/folders can be drag and dropped to te desired sub repo in dbt Cloud UI

3. good to know for the `dbt_profile.yml`

    - its a file that defines a project and paths where most needed config files are to be found

    - can determine things like what profile dbt should run under, what type od table models dbt should be creating etc

    - changed project name to `taxi_rides_ny` (lines 5 and 39)

### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1xSll_jv0T8JF4rYZvLHfkJXYqUjPtThA/edit#slide=id.p1)

* Lesson YT [video](https://www.youtube.com/watch?v=J0XCDyKiU64&list=PLaNLNpjZpzwgneiI-Gl8df8GCsPYp_6Bs&index=5)

* week4 [repo page](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/04-analytics-engineering)

* dbt [documnetation page](https://docs.getdbt.com/docs/introduction)

* Links for helping set up DBT:

    - Github [page](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/dbt_cloud_setup.md) to set up dbt Cloud with Bigquery

    - Github [dbt-core with BigQuery setup](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/docker_setup/README.md) (if not interested in using dbt Cloud)
