-- created_at: 2026-01-22T09:27:03.366260+00:00
-- finished_at: 2026-01-22T09:27:03.757644+00:00
-- elapsed: 391ms
-- outcome: success
-- dialect: databricks
-- node_id: not available
-- query_id: 01f0f774-82fa-1dcb-8f31-0ab6c2fd75f0
-- desc: execute adapter call
/* {"app": "dbt", "connection_name": "", "dbt_version": "2.0.0", "profile_name": "default", "target_name": "dev"} */
show databases;
-- created_at: 2026-01-22T09:27:04.400694+00:00
-- finished_at: 2026-01-22T09:27:04.892383+00:00
-- elapsed: 491ms
-- outcome: success
-- dialect: databricks
-- node_id: model.apnea_predictor.my_first_dbt_model
-- query_id: 01f0f774-8399-119d-a2e8-727ccffea58b
-- desc: get_relation > list_relations call

SELECT
    table_name,
    if(table_type IN ('EXTERNAL', 'MANAGED', 'MANAGED_SHALLOW_CLONE', 'EXTERNAL_SHALLOW_CLONE'), 'table', lower(table_type)) AS table_type,
    lower(data_source_format) AS file_format,
    table_schema,
    table_owner,
    table_catalog,
    if(
    table_type IN (
        'EXTERNAL',
        'MANAGED',
        'MANAGED_SHALLOW_CLONE',
        'EXTERNAL_SHALLOW_CLONE'
    ),
    lower(table_type),
    NULL
    ) AS databricks_table_type
FROM `system`.`information_schema`.`tables`
WHERE table_catalog = 'workspace'
    AND table_schema = 'dbt_jphelan';
-- created_at: 2026-01-22T09:27:05.086735+00:00
-- finished_at: 2026-01-22T09:27:05.545563+00:00
-- elapsed: 458ms
-- outcome: success
-- dialect: databricks
-- node_id: model.apnea_predictor.stg_test
-- query_id: 01f0f774-8401-1f88-8c0b-7b7c2f8e3724
-- desc: get_relation > list_relations call

SELECT
    table_name,
    if(table_type IN ('EXTERNAL', 'MANAGED', 'MANAGED_SHALLOW_CLONE', 'EXTERNAL_SHALLOW_CLONE'), 'table', lower(table_type)) AS table_type,
    lower(data_source_format) AS file_format,
    table_schema,
    table_owner,
    table_catalog,
    if(
    table_type IN (
        'EXTERNAL',
        'MANAGED',
        'MANAGED_SHALLOW_CLONE',
        'EXTERNAL_SHALLOW_CLONE'
    ),
    lower(table_type),
    NULL
    ) AS databricks_table_type
FROM `system`.`information_schema`.`tables`
WHERE table_catalog = 'workspace'
    AND table_schema = 'dbt_jphelan';
-- created_at: 2026-01-22T09:27:05.551017+00:00
-- finished_at: 2026-01-22T09:27:06.685925+00:00
-- elapsed: 1.1s
-- outcome: success
-- dialect: databricks
-- node_id: model.apnea_predictor.stg_test
-- query_id: 01f0f774-8448-101d-a77c-551148b2060a
-- desc: execute adapter call
/* {"app": "dbt", "dbt_version": "2.0.0", "node_id": "model.apnea_predictor.stg_test", "profile_name": "default", "target_name": "dev"} */
create or replace view `workspace`.`dbt_jphelan`.`stg_test`
  
  
  
  as
    -- models/staging/
SELECT
*
FROM `workspace`.`dbt_jphelan`.`stages_dataset_0_3_0`;
-- created_at: 2026-01-22T09:27:04.897999+00:00
-- finished_at: 2026-01-22T09:27:07.283766+00:00
-- elapsed: 2.4s
-- outcome: success
-- dialect: databricks
-- node_id: model.apnea_predictor.my_first_dbt_model
-- query_id: 01f0f774-83e4-1282-994d-a2548ad281b3
-- desc: execute adapter call
/* {"app": "dbt", "dbt_version": "2.0.0", "node_id": "model.apnea_predictor.my_first_dbt_model", "profile_name": "default", "target_name": "dev"} */
create or replace table `workspace`.`dbt_jphelan`.`my_first_dbt_model`
      
      
    using delta
  
      
      
      
      
      
      
      
      as
      
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/



with source_data as (

    select 1 as id
    union all
    select null as id

)

select *
from source_data

/*
    Uncomment the line below to remove records with null `id` values
*/

 where id is not null;
-- created_at: 2026-01-22T09:27:07.289143+00:00
-- finished_at: 2026-01-22T09:27:07.841146+00:00
-- elapsed: 552ms
-- outcome: success
-- dialect: databricks
-- node_id: model.apnea_predictor.my_second_dbt_model
-- query_id: 01f0f774-8551-13a9-ae59-8e323e911c02
-- desc: execute adapter call
/* {"app": "dbt", "dbt_version": "2.0.0", "node_id": "model.apnea_predictor.my_second_dbt_model", "profile_name": "default", "target_name": "dev"} */
create or replace view `workspace`.`dbt_jphelan`.`my_second_dbt_model`
  
  
  
  as
    
-- Use the `ref` function to select from other models

select *
from `workspace`.`dbt_jphelan`.`my_first_dbt_model`
where id = 1;
