create table gold_events as
select distinct 
global_event_id, sqldate, is_root_event, event_code,
       event_base_code, event_root_code, quad_class, goldstein_scale,
       num_mentions, num_sources, num_articles, avg_tone,  action_geo_country_code,
       source_url
from parquet_external_schema.events
where action_geo_country_code is not null and event_root_code = '0'