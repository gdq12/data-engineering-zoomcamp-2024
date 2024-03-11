### Background of dbt Models

* Models consists of jinja syntax (pythonic centric language)

    - this allows for macro implementation and data linege modeling

    - in the end dbt will use the model scripts to compile create* queries and send the commands to the DWH for sql execution

* materilaized strategies

    - `table` and `views`: they are self explantory

    - `incremental`: run model incrementally, best for data that doesn't change every day, permits only new records to be added to the table

    - `ephemeral`: its like a CTE/subquery, it is embedded in another file, its a derived model

* models:

    - it is the directory in which the transformations of dbt are derived from

    - each subdirectory within this directory represents a schema

    - each of these subdirectories/schema will have a `schema.yml` file. this also auto builds dependencies

* types of data sources

    - sources

        + data that is loaded into the DWH for transformations (typically raw data)

        + configuration of these tables are define in a yml file in the models directory

        + they are defined by a source macros which: resolves tbl/schema name, auto determine dependencies, freshness of the data can be resolved and tested

    * seeds

        + they are CSV files that are stored in the `seeds` directory of the repo

        + best practice would be to use this approach for data the doesn't change often

        + dbt auto compiles a copy command to have this pushed into the DWH: `dbt seed -s fileName`

* macro syntax explanations

    - `{{ config(materalized='table') }}`: method to define a materlialized table (other method is via the `schema.yml` in each respective model folder). it allows from a dev/prod point of view to create tables in the different respective schemas without having to manually make the change when the model goes from dev to test

    - `{{ source ('shema_name', 'tbl_name') }}`: this indicates a table that was not created from dbt's transformation mechanism. It is data that is loaded to a respective data warehouse, typically in its raw format. This is one of the types of data sources that a fiven from clause will extract from.

    - `{{ ref('tbl_name') }}`: this indicates that a table created by dbt transformation is being called upon. there is no need to include the schema name in it because this is resolved via the respective yml file

### Modeling in dbt

- work here is done in the `models` directory

- model: `staging`

    - handles transformation of raw data

    - `schema.yml`

        + it defines from which dataset/schema/tables the source for this modeling will come from

            ```{sql}
            version: 2

            sources:
            - name: staging
                database: ny-taxi-412905
                schema: nytaxi_wk4_dbt_raw

                tables:
                - name: external_green_trip_data
                - name: external_yellow_trip_data
                - name: external_fhv_trip_data
            ```

    - `stg_grn_dataset.sql`

        + this is an sql file that will be compiled to `create or replace view as ......`

            ```{sql}
            {{ config(materialized='view') }}

            select
                -- identifiers
                {{ dbt_utils.generate_surrogate_key(['vendor_id', 'lpep_pickup_datetime']) }} as tripid,
                {{ dbt.safe_cast("vendor_id", api.Column.translate_type("integer")) }} as vendorid,
                {{ dbt.safe_cast("ratecode_id", api.Column.translate_type("integer")) }} as ratecodeid,
                {{ dbt.safe_cast("pu_location_id", api.Column.translate_type("integer")) }} as pickup_locationid,
                {{ dbt.safe_cast("do_location_id", api.Column.translate_type("integer")) }} as dropoff_locationid,

                -- timestamps
                cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
                cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,

                -- trip info
                store_and_fwd_flag,
                {{ dbt.safe_cast("passenger_count", api.Column.translate_type("integer")) }} as passenger_count,
                cast(trip_distance as numeric) as trip_distance,
                {{ dbt.safe_cast("trip_type", api.Column.translate_type("integer")) }} as trip_type,

                -- payment info
                cast(fare_amount as numeric) as fare_amount,
                cast(extra as numeric) as extra,
                cast(mta_tax as numeric) as mta_tax,
                cast(tip_amount as numeric) as tip_amount,
                cast(tolls_amount as numeric) as tolls_amount,
                cast(ehail_fee as numeric) as ehail_fee,
                cast(improvement_surcharge as numeric) as improvement_surcharge,
                cast(total_amount as numeric) as total_amount,
                coalesce({{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }},0) as payment_type,
                {{ get_payment_type_description("payment_type") }} as payment_type_description
            from {{ source('staging', 'external_green_trip_data') }}
            limit 100
            ```

        + good to knows about the the above sql:

            - it transforms the raw data copied over from gcs to the correct column names and data types

            - `{{ dbt_utils.generate_surrogate_key(['vendor_id', 'lpep_pickup_datetime']) }}`: creates a unique key for the view

            - `{{ get_payment_type_description("payment_type") }}`: calls upon a macro to create a case statement for code compilation

            - there are custom macros and dbt base packages that must be defined in order to `dbt run --select stg_grn_dataset` successfull:

                - `packages.yml`: defines which dbt packages and respective version need to be loaded to a job IDE for the compilation to be successful.

                - `macros/get_payment_type_description.sql`: macros that is essentially a case statement to be run in the called view/table compilation.

* when the models are run, the compiled code is saved in `target` directory. By default this directory is in `.gitignore` but it can be removed from there to keep a version history of the compiled code.

### Macros

* functions written in jinja

* they are like python functions in that they expect certain parameters and return specific a code

* good to maintain same type of transformations across models

* they are created in the `macros` directory and use a mix of sql and jinja

* example macros `get_payment_type_description.sql`

  ```{sql}
  {#
      This macro returns the description of the payment_type
  #}

  {% macro get_payment_type_description(payment_type) -%}

      case {{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }}  
          when 1 then 'Credit card'
          when 2 then 'Cash'
          when 3 then 'No charge'
          when 4 then 'Dispute'
          when 5 then 'Unknown'
          when 6 then 'Voided trip'
          else 'EMPTY'
      end

  {%- endmacro %}
  ```

  * `% .... %`: signifies that something is being executed

  * `macro ..... endmacro` defines the code/sql that should be returned

  * `{{ val_name }}` is the input that will be translated by the macros when fed from the model file

### Packages

* use macros from dbt

* dbt projects that have models/macros that can be imported to target project

* can find more packages in dbt package hub or github

* they are called upon into the working project within the `project.yml`:

  ```
  packages:
    - package: dbt-labs/dbt_utils
      version: 1.1.1
    - package: dbt-labs/codegen
      version: 0.12.1
  ```  

* they are also called upon in models using jinja syntax. They are encapsulated within `{{ .... }}` along with their input parameters (which are often columns of the query table)

* to download the packages, will need to download all dependencies via `dbt deps`

  * this create a directory `dbt_packages` which consists of the downloaded code used to compile the packages for runs

### Variables

* efficient way to define variable that can be used across the project

* they are provided to models via macros

* to define global variables (those to be used across models), they can be defined in the `dbt_project.yml` file

  ```
  vars:
    payment_type_values: [1, 2, 3, 4, 5, 6]
  ```

* they can be defined in the terminal with dbt CLI:

  ```
  {% if var('is_test_run', default = true) %}

  limit 100

  {% endif %}
  ```

    - this is another way to add `limit x` to the end of a query for data limitation

    - when this macros is inserted into a model sql file, it can be altered during dbt commands: `dbt build --m <model.sql> --var 'is_test_run: false'`. This changes the `is_test_run` value from `true` to `false`. When it is changes to false, then the `limit x` syntax is removed from the query. The difference can be seen in `target/compiled/taxi_rides_ny/models/staging/stg_grn_dataset.sql`

### dbt Seeds

* to load SMALL csv files into the data model

* there are several ways to load a csv file: when working locally simply add it to the `seeds` directory, can pull the file from github to dbt Cloud when its already in the correct directory, or can add it manually via the dbt cloud UI

* run `dbt seed` in order to create a new table in the transform schema. New table will be `ny-taxi-412905.nytaxi_wk4_dbt_transform.taxi_zone_lookup`

* when generating the seed table(s) can also custom define the column types in the `dbt_project.yml` file

  ```
  models:
    taxi_rides_ny:
      # Applies to all files under models/example/
      example:
        +materialized: table

  seeds:
    taxi_rides_ny:
      taxi_zone_lookup:
        +column_types:
          locationid: numeric
  ```

  + can either custom determine all data types or only some data types

* `dbt seed`

  + when it is run for the first time, it does a create table

  + when its run for consecutive times with the values in the csv file changing, it will just do an incremental load and only insert new values into the table

  + to do a full refresh post first time run: `dbt seed --full-refresh`

* `dbt run`

  + this will not compile the seed tables

* `dbt build`

  + it build EVERYTHING (seeds and test)

### Overview of dbt CLI commands

* `dbt run`

  + compiles the all the packages, macros and models to verify that it will come out correctly

  + `--select <model_name>`: adding this executes the run command on only a single model file

* `dbt build`

  + it builds ALL models, tables, views, seeds etc

  + `--select +<model_name>`: the `+` sign tell dbt to also compile the the models that the target model name are dependent on. placing the `+` after the model name tells dbt to also run the models that are dependent on the target model name

### Helpful Links

* YT [lecture](https://www.youtube.com/watch?v=ueVy2N54lyc&list=PLaNLNpjZpzwgneiI-Gl8df8GCsPYp_6Bs&index=4)

* Lecture [slides](https://docs.google.com/presentation/d/1xSll_jv0T8JF4rYZvLHfkJXYqUjPtThA/edit#slide=id.p1)
