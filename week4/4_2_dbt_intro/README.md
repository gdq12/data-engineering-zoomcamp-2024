### DBT Background 

* DBT = Data Build Tool 

* permits individuals with SQL skills transform data while implementing software engineering best practices 

* helps define a development workkflow: 

    * develop models 

    * test document 

    * deployment phase: version control along with CI/CD

### DBT functionality 

* components 

    * raw data source (DWH)

    * containerized environment (prob outside of the DWH?) that transforms the data. Known as the modeling layer 

* the modeled data is persisted back to the DWH 

* model compiling 
    
    * models are written in sql files (select statement w/o DDL or DML)

    * DBT then compiles the file and sends the sql command back to the DWH    

    * the actualy computing transforming occurs int eh DWH, just the compilation of code occurs within a DBT container 

### DBT uses

* dbt Core 

    * the essense of dbt 

    * open-source project that permits data transformations 

    * part that builds and runs the project 

    * does that actual compilations based on the used macros and DHW plugins 

    * open source and free to use 

    * command line interphase

* dbt Cloud 

    * web application 

    * dev nd manage project 

    * permits orchestration, logging, alerts etc 

    * has documentation integration 

    * free for single user use, paid for company use 

### Using dbt for the course

* with BigQuery, will be using dbt Cloud

* if using postgres, using dbt local

* use trip data outlined/listed [here](https://github.com/DataTalksClub/nyc-tlc-data/)

* dbt will be transformed via dbt 

* examine it in a dashboard 

### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1xSll_jv0T8JF4rYZvLHfkJXYqUjPtThA/edit#slide=id.p1)

* Github [page](https://github.com/DataTalksClub/nyc-tlc-data/) for data needed for dbt project 

* dbt [documnetation page](https://docs.getdbt.com/docs/introduction)

* Lesson YT [video](https://www.youtube.com/watch?v=4eCouvVOJUw)