### I. Adding Taxi Zone info with taxi data

1. ran the following python script to populate db locally not in docker 
    
    ```python
    import pandas as pd
    from sqlalchemy import create_engine
    from datetime import datetime
    
    # fetch data from ny taxi website
    print(f"fetching jan 2021 nyc taxi data on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet'
    df = pd.read_parquet(url, engine = "fastparquet")
    
    # fetch lookup table
    print(f"fetching taxi look up data on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    url1 = 'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
    df1 = pd.read_csv(url1)
    
    # connecting to postgres
    user = 'postgres'
    pwd = 'root'
    db_name = 'postgres'
    port = 5432
    host = 'localhost'
    
    print(f"connecting to postgres docker container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
    conn = engine.connect()
    
    print(f"creating a new database on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}" )
    db_name = 'ny_taxi'
    conn.execute('commit')
    conn.execute(f'create database {db_name}')
    conn.execute('commit')
    conn.close()
    
    print(f"connecting to postgres docker container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
    conn = engine.connect()
    
    # create table with column names in postgres
    print(f"creating yellow_taxi_data table in postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    df.head(n = 0).to_sql(name = 'yellow_taxi_data', con = conn, if_exists = 'replace', index = False)
    
    # create zone tablein postgres
    print(f"creating taxi zone lookup table in postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    df1.head(n = 0).to_sql(name = 'taxi_zone_lookup', con = conn, if_exists = 'replace', index = False)
    
    # push the rest of data into table
    print(f"populating yellow_tax_table on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    df.to_sql(name = 'yellow_taxi_data', con = conn, if_exists = 'append', index = False)
    
    # push the rest of data into table
    print(f"populating taxi_zone_lookup on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    df1.to_sql(name = 'taxi_zone_lookup', con = conn, if_exists = 'append', index = False)
    
    # close connex
    print(f"data push complete and closing connection to postgres container on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    conn.close()
    ```
    

### II. EDA with Queries

```sql
-- example of inner join 
select 
	t1.tpep_pickup_datetime,
	t1.tpep_dropoff_datetime,
	t1.total_amount,
	t2."Borough"||' '||t2."Zone" as pick_up_loc,
	t3."Borough"||' '||t3."Zone" as drop_off_loc
from 
	yellow_taxi_data t1,
	taxi_zone_lookup t2,
	taxi_zone_lookup t3 
where 
	t1."PULocationID" = t2."LocationID" and
	t1."DOLocationID" = t3."LocationID"
limit 100
;

-- another way to write joins 
select 
	t1.tpep_pickup_datetime,
	t1.tpep_dropoff_datetime,
	t1.total_amount,
	t2."Borough"||' '||t2."Zone" as pick_up_loc,
	t3."Borough"||' '||t3."Zone" as drop_off_loc
from yellow_taxi_data t1 
join taxi_zone_lookup t2 on t1."PULocationID" = t2."LocationID" 
join taxi_zone_lookup t3 on t1."DOLocationID" = t3."LocationID"	
limit 100
;

-- do spot check on data
select * 
from yellow_taxi_data 
--	where tpep_pickup_datetime is null 
--	where tpep_dropoff_datetime is null
--	where total_amount is null
--	where total_amount = 0
--	where "PULocationID" not in (select "LocationID" from taxi_zone_lookup)
	where "DOLocationID" not in (select "LocationID" from taxi_zone_lookup)
;

-- testing validity of missing records by deleting a record in taxi_zone_lookup
delete from taxi_zone_lookup where "LocationID" = 142;

-- left join to verify all records from yellow_taxi_data still appears 
select 
	t1.tpep_pickup_datetime,
	t1.tpep_dropoff_datetime,
	t1.total_amount,
	t2."Borough"||' '||t2."Zone" as pick_up_loc,
	t3."Borough"||' '||t3."Zone" as drop_off_loc
from yellow_taxi_data t1 
left join taxi_zone_lookup t2 on t1."PULocationID" = t2."LocationID" 
left join taxi_zone_lookup t3 on t1."DOLocationID" = t3."LocationID"
limit 100
;	

SELECT
--	cast(tpep_dropoff_datetime as date) as dates, -- another way to extract day from timestamp col
	date_trunc('DAY', tpep_dropoff_datetime) as dates,
	"DOLocationID", 
	count(1),
	max(total_amount),
	min(passenger_count)
from yellow_taxi_data
--	where date_trunc('DAY', tpep_dropoff_datetime) != date_trunc('DAY', tpep_pickup_datetime) -- determine where rides crossed over into the next/previous day
	group by 
--		date_trunc('DAY', tpep_dropoff_datetime)
		1, 2 -- can also use number instead of typing out whole column name 
		order by 3 desc
;
```

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=QEcps_iskgg&t=65s)

* Lecturer's [notes](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)