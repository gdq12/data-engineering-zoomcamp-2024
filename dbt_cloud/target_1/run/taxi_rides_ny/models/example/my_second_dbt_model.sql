
  
    

    create or replace table `ny-taxi-412905`.`nytaxi_wk4_dbt_transform`.`my_second_dbt_model`
      
    
    

    OPTIONS()
    as (
      -- Use the `ref` function to select from other models

select *
from `ny-taxi-412905`.`nytaxi_wk4_dbt_transform`.`my_first_dbt_model`
where id = 1
    );
  