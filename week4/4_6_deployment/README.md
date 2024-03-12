### Deployment Background

* once coding and dev are complete deployment is the next step

* pull request to main --> affect production

* deployment work flow works in different database/schemas compared to dev --> permits for paralell changes of prod and dev without dev being affected

* there is also the possibility for scheduling of updates to occur

* highlight of ideal workflow:

  - development in a non-main branch

  - merge completed dev to main branch via git PR

  - run new models in prod via main branch

  - schedule the full/incremental refreshes

* dbt scheduler:

  - it creates jobs that can be run multiple times

  - a single job can run multiple commands/steps etc

  - can be triggered via cron or API

  - additional steps can be implemented like doc generation and log info for each run can be viewed as well

### Steps to deploy Project

**make sure dev code push to main branch before going through process**

1. in dbt Cloud click `Deploy` > `Environment`

2. Create a new Production environment via `+ Create environment`

  - Environment Name: Production

  - set deployment type: PROD

  - Dataset: nytaxi_wk4_dbt_prod (name of schema where `models/core` should be created/updated)

  - everything else default

3. `+ Create job` > `Deploy job`

  - Job name: Nightly (descriptive to purpose)

  - Description: '1-liner sentence'

  - Environemtn: Production (what was created in step 2)

  - Commands: `dbt build` (defualt option but can be changed)

  - Generate docs on run: check

  - Run source freshness: check

  - Run on schedule: yes

  - timing: on specific time/hour

  - run at (UTC): 12

  - days of week: mon-fri

4. Trigger via `> Run now`

* additional methods of triggering: `</> API trigger`

  - pop-up window in terms of the API syntax needed for this to occur.

  - documentation link page also available

5. Inspection of run logs:

  - SHA link of github link can be visited to see what changes took place in the code when the code was deployed

  - clones the main branch to dbt Cloud

  - connect to target DWH

  - `dbt deps`: to install dbt packages

  - `dbt source freshness`: think this is to execute a full data refresh

  - `dbt build`: compile coded models

  - `dbt docs generate`: create the documentation from yaml files

  - UI also lists the artifacts produced during run like compiled sql code and jsons

  - can also decide from which job the documentation should be hosted in. This can be done by going to project settings and under artifacts selecting the project name.

### CI/CD integration

* CI: continuous integratoin aka always merging dev branches to main then auto buiding/testing

* CD: continuous deployment

* goal is to make very micro changes to reduce bug add to the prod code and maintain a stable project

* enabling this via dbt Cloud

  - under `Deploy` > `Production` > `+ Create job` select continuous integration

  - Job name: CI checks

  - Description: 1-lines description

  - Environment: Production

  - Trigger by pull request: check (creates a temp schema in DWH)

  - Commands: `dbt build --select state:modified+` (model that have been updated and the children models), `dbt test documented_models` (test that will fail if the models aren't documented)

  - compare changes against an environment (deferral): Production

- with the previous bull points set up, a run will be auto triggers when the dev branch is merged to main --> triggering github CI/CD mechanism

### Observations

* based on the current settings from this week's lessons, it appears that dev views/tables are created in `ny-taxi-412905.nytaxi_wk4_dbt_transform` and the deployed ones are in `ny-taxi-412905.nytaxi_wk4_dbt_prod`

* it would be ideal if the model produced in `models/stage` and created in `ny-taxi-412905.nytaxi_wk4_dbt_transform` and those in `models/core` be created in `ny-taxi-412905.nytaxi_wk4_dbt_prod`


### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1xSll_jv0T8JF4rYZvLHfkJXYqUjPtThA/edit#slide=id.p1)

* YT [video](https://www.youtube.com/watch?v=V2m5C0n8Gro&list=PLaNLNpjZpzwgneiI-Gl8df8GCsPYp_6Bs&index=7)
