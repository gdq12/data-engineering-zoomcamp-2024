### Analytics Engineering Role 

* came about from the domain development:

    * cloud DWH: lower cost of storage 

    * five-trina/stitch: simplify ETL process

    * SQL-first/looker: version control of data workflow

    * Mode(BI-tool): self service analytics 

    * data governance 

* changed the way stakeholders consume data 

* gap created in data teams

    * data engineer: prepare and maintain data structure, good software engineer but dont have the business knowledge 

    * data analyst: get insights from data 

    * data scientist: write more code but are not software engineers

* analytics engineer: mix of software engineer with the business part of analyst and scientist 

* tools 

    * data loading

    * data storage (Bigquery, snowflake, redshift) 

    * data modeling (DBT)

    * data presentation (Looker, Mode, Tableau)

### Data Modeling Concepts 

* ETL: extract --> transform --> load 

    * more work to implement 

    * more stable and compliant data 

* ELT: extract --> load --> transform 

    * faster and more flexible

    * can lower costs 

### Modeling 

* based on Kimball's Dimensional Modeling 

* it is meant to make the data understandable to the user and can be delivered quickly via queries 

* make understandability and query performance more of a priority over data redundancy 

* other interesting approaches: Bill Inmon and Data Vault

* Dimensional Modeling (star schema) 

    * fact tables: consists of measurements and metrics, correspond to a business process, they describe the business (verbs). ex: sales, orders

    * dimensional tables: corresponds to a business entity, provide business context, ex: customer, product. they are the nouns of the model 

* Architecture (kitchen analogy)

    * stage area (groceries): raw data, only for ppl that understand the raw data 

    * processing area (kitchen for cooking): transformation models, for efficienty and good standards followed 

    * presentation area (dining table to serve final product): final presentation of data, exposure to business stakeholders 

### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1xSll_jv0T8JF4rYZvLHfkJXYqUjPtThA/edit#slide=id.p1)

* Github [page](https://github.com/DataTalksClub/nyc-tlc-data/) for data needed for dbt project 

* dbt [documnetation page](https://docs.getdbt.com/docs/introduction)

* Lesson YT [video](https://www.youtube.com/watch?v=uF76d5EmdtU&t=2s)