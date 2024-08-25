create table gold_gkg_counts as
select distinct 
geo_country_code ,numarts, count_type, "number", cameo_event_ids
from parquet_external_schema.gkg_counts