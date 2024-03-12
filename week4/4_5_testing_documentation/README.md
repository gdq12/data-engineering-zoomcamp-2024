### dbt Test

* try to verify that the models are using good data

* assumptions that we make about the data

* they are essentially select statements that aim to filter out unwanted data

* will halt model development when an error is caught

* dbt out of the box test functions: unique, not null, accepted values and foreign keys

* warning is rendered in CLI when a test fails

* during `dbt build` or `dbt run` the models are first built, then the test are executed. This process is followed for each layer of the lineage (staging, transformation, prod etc.)

* test implementation syntax:

  ```
  models:
    - name: tbl_name
      description: ""
      columns:
        - name: col_name
          data_type: int64
          description: ""
          tests:
            - unique:
              severity: warn
           - not null:
              severity: warn
          - relationships:
              field: foreign_key
              to: ref('tbl_name_foreign_key')
              severity: warn
          - accepted_values:
              values:
                - [1,2,3,4,5]
              values: "{{ var('col_name') }}"
              severity: warn
              quote: false
  ```

  + good to knows

    - `severity: warn`: this indicates that the model building should still occur but to just give a warning in the CLI that the column did not meet the test

    - `relationships`: this test is to verify that there are no surprising values in that column. That all value present are derived from the foreignkey column. `field` and `to: ref()` define the foreign key and foreign key table respectively

    - `values`: there are 2 ways to define this test. The values can either be hard code defined (values stored in an array) OR they are defined by calling upon the global variable defined in `dbt_project.yml`

    - `quote: `: this is a Bigquery specific syntax. Hypothesize that it is telling dbt underlying python code to exclude unintentional quotation marks when passing sql string to Bigquery.

### Macros

* [cross-database macros](https://docs.getdbt.com/reference/dbt-jinja-functions/cross-database-macros)

* to adapts certain sql functions accroding to the underlying sql flavor. Functions have different syntax from DWH to DWH

* codegen: [dbt documentation](https://hub.getdbt.com/dbt-labs/codegen/latest/), [github page](https://github.com/dbt-labs/dbt-codegen)

  - its a package provided by dbt which works under the hood when run

  - its a package that helps develop yaml files for each model within a schema. The info should then be saved in `schema.yml`

  - methods to call the function

    + in dbt CLI: `dbt run-operation generate_source --args 'schema_name: staging'`

    + in dbt cloud with the `compile` function (have the text copy pasted in an unsaved file in the IDE):

      ```
      {% set models_to_generate = codegen.get_models(directory='staging', prefix='stg_') %}
      {{ codegen.generate_model_yaml(
          model_names = models_to_generate
      ) }}
      ```

### dbt Documentation

* add documentation to every project in dbt: for models that are created in dbt and for source tables that aren't created in dbt

* components that are provided:

  - how the models come together (based on the model.sql files and how they are compiled together)

  - rendering data lineage via model dependencies (from code and DAGs)

  - descriptions rendered from `yaml` files

* it can also pull info from the DWH: column names/data types and table stats stored in the information_schema

* once all model code is complete (testing etc.) and yaml files have been correctly filled in (`dbt_project.yml`, `schema.yml`) dbt can compile and host documentation pages on its server (local or cloud) with the following command: `dbt docs generate`. The results of this can be viewed in 2 ways:

  - in dbt Core (local development) and local IP address will be provided in the command line that can be visited

  - in dbt Cloud it can be visited by clicking on the small open book icon at the top right corner of the left hand panel (next to the github branch name).


### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1xSll_jv0T8JF4rYZvLHfkJXYqUjPtThA/edit#slide=id.p1)

* YT [video](https://www.youtube.com/watch?v=2dNJXHFCHaY&list=PLaNLNpjZpzwgneiI-Gl8df8GCsPYp_6Bs&index=3)
