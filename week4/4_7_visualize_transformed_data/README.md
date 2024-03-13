### Background of Data Studio (Formally Looker)

* its a dashboard tool provided by GCS, it can be found in [datastudio/looker link](datastudio.google.com)

* load and build dashboard with the same general method as QS from QWS

### Steps to build dashboard

1. go to the dashboard tool homepage

2. load the datasource to its server

  * go to `Data sources` found in recent

  * click on `+ Create` to Bigquery data source

  * agree to permit looker to access bigquery datasets

  * select the following:

    - project: ny-taxi

    - dataset: ny_taxi_dbt_prod

    - table: fact_trips

  * `Connect`

3. Looker will automatically examine each column/dimension, derive the data type and determine what aggregation to apply to them. Best to disable that where it is not optimal

4. Optional: can provide description fields in each of the imported columns --> optimal for audience that will view the created reports

5. Optional: can also determine the schedule of how often the data should be refreshed  

6. Optional: changed the name of the table source at the top left hand corner. This is ideal when the table is shared with stakeholders to a more user friendly term

7. click `CREATE REPORT` top right hand corner

8. Editing the report: the interphase UI quite similiar to QS AWS so create reports by adding chart and customizing the fields according to what data needs to be graph and in which outcome is needed

### Helpful links

* YT [video](https://www.youtube.com/watch?v=39nLTs74A3E&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=49)
