### Background on type of DWHs 

* OLTP (online transaction processing)

    - usually used in backend services, do some role backs if needed 

    - updates/change are fast but small 

    - should be normalized for efficieny 

    - productivity increased for end user

    - online shopping, customer facing 

* OLAP (online analytical processing)

    - used for data aggregations and insights 

    - data updates are done periodically with long running batch jobs 

    - mostly used for analyst etc 

    - this is what a DWH is 

### Data warehouse 

- OLAP solution used for reporting and data analysis 

- raw data --> stage area --> warehouse --> data marts --> consumed by different users

- analyst usually use data marts

- data scientist usually look at raw data 

### BigQuery 

- its a serveless DWH (google takes care of the software maintenance, infra etc.)

- scalability is very easy (size is not an issue)

- it acts like snowflake: it seperates the computing and analyze data from storage 

- to do when using big query: 

    - go to settings and uncheck using cache setting

    - there is a lot of publi data available, it is in `biquery-public-data`

- can use data studio to explore data 

- pricing models: on demand or flat rate (best when using more than 200TB a month)

- can create tables from buckets (external sources)

    - bigquery can already recognize data type 

    - bigquery cant determine data dimensions until its imported into bigquery 

- partitions

    - improves the performance immensly 

    - most of the time data is partitioned by date 

    - it saves the engine from scanning data that is not of interest (reduction in data volume scan)

    - bigquery UI have different icons for partitioned vs non-partitioned tables 

    - can see the volume of each partition via the `<schema_name>.information_schema.partitions`

- clusters 

    - clustering is like creating subsets in the partitions --> so its like using 2 columns to chunk the data 

    - also helps improve cost and performance 

    -  deciding what to cluster is dependent on how one plans to query the data. If one knows the EDA queries will be based on a column, best to choose it for clustering.

    - clustering reduces data scan volume even more.

### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit#slide=id.g10eebc44ce4_0_26)

* YT [video](https://www.youtube.com/watch?v=jrHljAoD6nM&t=7s)

* Query [sheet](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/03-data-warehouse/big_query.sql)