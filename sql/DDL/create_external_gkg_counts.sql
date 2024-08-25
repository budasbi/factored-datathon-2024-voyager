CREATE EXTERNAL TABLE `voyager_lake.gkg_counts`(
  `numarts` string, 
  `count_type` string, 
  `number` string, 
  `object_type` string, 
  `geo_type` string, 
  `geo_fullname` string, 
  `geo_country_code` string, 
  `geo_adm1_code` string, 
  `geo_lat` string, 
  `geo_long` string, 
  `geo_feature_id` string, 
  `cameo_event_ids` string, 
  `sources` string, 
  `source_urls` string)
PARTITIONED BY ( 
  `date` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://factored-datathon-2024-voyager/parquet/gkg_counts/'
TBLPROPERTIES (
  'CrawlerSchemaDeserializerVersion'='1.0', 
  'CrawlerSchemaSerializerVersion'='1.0', 
  'UPDATED_BY_CRAWLER'='gkgcounts', 
  'averageRecordSize'='4030', 
  'classification'='parquet', 
  'compressionType'='none', 
  'objectCount'='850', 
  'partition_filtering.enabled'='true', 
  'recordCount'='11567365', 
  'sizeKey'='10056185489', 
  'typeOfData'='file')