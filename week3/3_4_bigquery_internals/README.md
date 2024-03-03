### Colossus: Bigquery Storage 

- bigquery stores data in cheap storage called colossus in columnar fashion 

- seperate storage from computing power, which reduces cost, so no matter how much more data is added cost will not increased 

### Jupiter: Bigquery Network

- since data storage and computing are kept in seperate layers, it is quite dependent on how well they are connected with each other 

- if there is bad connectivity between the 2, in can result in high query time which drives up cost 

- this is resolved via jupiter network comes into play

    - they reside in bigquery data centers and provide 1TB/sec network speed 

    - this reduces delay over network 

### Dremel: Bigquery Computing Engine 

- this engine internally divides the query into 3 structures 

    - root nodes 
    
    - intermediate node/mixers

    - leaf nodes (local storage) 

- leads to each subset of a query to be executed by a single node 

### Columnar vs Record Oriented Storage 

- record oriented structure (aka row) similiar to excel and csv structures --> easy to process/understand 

- column oriented strucuture (columns)

    - rows can be seen in multiple columns 

    - helps provide better aggregations 

    - usually not all columns are queried at 1 time 

### Query processing by Bigquery 

- steps of query evaluation:

    1. query compiled and sent to Dremel root server  
    
    2. divides query by smaller submodules (R1-R1n)

    3. modified query from step 2 are sent to mixers 

    4. divided to further subqueries 

    5. further divided queries given to leaf nodes 

    6. leaf nodes communicate with the colossus data base 

    7. the resulting data table is returned to the mixers --> then to the root server 

- distribution of servers is the big advantage with bigquery 

    - the query is subsetted and distributed to individual nodes rather than having it being executed in a single node like redshift 

### Helpful Links

* Lecture [slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit#slide=id.g10eebc44ce4_0_26)

* YT [video](https://www.youtube.com/watch?v=eduHi1inM4s&t=3s)

* Query [sheet](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/03-data-warehouse/big_query.sql)

* additional articles about Bigquery internals :

    - [Bigquery how to doc](https://cloud.google.com/bigquery/docs/how-to)

    - [research publication](https://research.google/pubs/pub36632/)

    - [Bigquery architecture](https://panoply.io/data-warehouse-guide/bigquery-architecture/)

    - [Dremel article](http://www.goldsborough.me/distributed-systems/2019/05/18/21-09-00-a_look_at_dremel/)