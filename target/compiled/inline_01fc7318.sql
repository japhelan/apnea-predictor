select * from (
with source_data as (

    select 1 as id
    union all
    select null as id

)
SELECT * FROM source_data
) as __preview_sbq__ limit 1000