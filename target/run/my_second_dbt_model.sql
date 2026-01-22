create or replace view `workspace`.`dbt_jphelan`.`my_second_dbt_model`
  
  
  
  as
    
-- Use the `ref` function to select from other models

select *
from `workspace`.`dbt_jphelan`.`my_first_dbt_model`
where id = 1
