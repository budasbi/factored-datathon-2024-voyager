import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as SqlFuncs
from awsglue.dynamicframe import DynamicFrame
import gc
import os 
import boto3
import pandas as pd

S3_BUCKET_NAME = 'factored-datathon-2024-voyager-temp'   
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


def get_not_processed_files(filetype):
    if filetype=='events':
        raw_folder = 'raw/events'
        parquet_folder = 'parquet/events'
        partition = 'date_added'
    elif filetype=='gkg_counts':
        raw_folder = 'raw/gkg_counts'
        parquet_folder = 'parquet/events'
        partition = 'date_added'
        
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=raw_folder)
    raw_files = pd.DataFrame(response['Contents'])
    raw_files['processed_date'] = raw_files['Key'].map(lambda x: x.split('/')[2].replace('year=','') + x.split('/')[3].replace('month=','')+ x.split('/')[4].replace('day=',''))
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=parquet_folder)
    parquet_files = pd.DataFrame(response['Contents'])
    parquet_files['parquet_date'] = parquet_files['Key'].map(lambda x: x.split('/')[-2].replace(f'{partition}','').replace('=','').replace('-','') )
    missing_files = pd.merge(raw_files, parquet_files, left_on='processed_date', right_on='parquet_date', how='outer', indicator='missing')
    missing_files = list(missing_files.loc[missing_files['missing']=='left_only', 'Key_x'].drop_duplicates())
    missing_files.map(lambda x: S3_BUCKET_NAME+'/'+x)
    return missing_files

list_to_process = get_not_processed_files('events')

# Script generated for node Amazon S3
events = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": False, 
                                                                       "separator": "\t", "optimizePerformance": False}, 
                                                       connection_type="s3", format="csv", connection_options={
                                                           "paths": list_to_process, "recurse": True}, transformation_ctx="events")



def cleaned_to_parquet(raw_df):
    spark_df = raw_df.toDF()
    # print(csv_filepath)
    #Set column names
    event_columns = ["global_event_id", "sqldate", "month_year", "year", "fraction_date", "actor_1_code", "actor_1_name", "actor_1_country_Code", "actor_1_known_group_code", "actor_1_ethnic_code", 
                    "actor_1_religion_code", "actor_1_religion_2_code", "actor_1_type_code", "actor_1_type_2_code", "actor_1_type_3_code", "actor_2_code", "actor_name", 
                    "actor_2_country_code", "actor_2_known_group_code", "actor_2_ethnic_code", "actor_2_religion_1_code", "actor_2_religion_2_code", 
                    "actor_2_type_1_code", "actor_2_type_2_code", "actor_2_type_3_code", "is_root_event", "event_code", "event_base_code", "event_root_code", 
                    "quad_class", "goldstein_scale", "num_mentions", "num_sources", "num_articles", "avg_tone", "actor_1_geo_type", "actor_1_geo_fullname", "actor_1_geo_country_code", 
                    "actor_1_geo_adm1_code", "actor_1_geo_lat", "actor_1_geo_long", "actor_1_geo_feature_id", "actor_2_geo_type", "actor_2_geo_fullname", "actor_2_geo_country_code", 
                    "actor_2_geo_adm1_code", "actor_2_geo_lat", "actor_2_geo_long", "actor_2_geo_feature_id", "action_geo_type", "action_geo_fullname", "action_geo_country_code", 
                    "action_geo_adm1_code", "action_geo_lat", "action_geo_long", "action_geo_feature_id", "date_added", "source_url"]
    event_w_columns = spark_df.toDF(*event_columns)
    #Cast date columns as date
    event_w_to_date = event_w_columns.withColumn('date_added', SqlFuncs.to_date('date_added', 'yyyyMMdd'))
    event_w_to_date = event_w_to_date.withColumn('sqldate', SqlFuncs.to_date('sqldate', 'yyyyMMdd'))
    # event_w_to_date.select(column).distinct().orderBy(column, ascending = False).show(5, truncate =False)
        

    #Set string columns Uppercase
    uppercase_columns=['actor_1_code','actor_2_code','actor_1_name','actor_1_country_Code','actor_1_known_group_code','actor_1_ethnic_code','actor_1_religion_code','actor_1_religion_2_code','actor_1_religion_2_code','actor_1_type_code','actor_1_type_2_code','actor_1_type_3_code','actor_2_code','actor_name','actor_2_country_code','actor_2_known_group_code','actor_2_ethnic_code','actor_2_religion_1_code','actor_2_religion_2_code','actor_2_type_1_code','actor_2_type_2_code','actor_2_type_3_code','actor_1_geo_country_code','actor_1_geo_adm1_code','actor_1_geo_feature_id','actor_2_geo_country_code','actor_2_geo_adm1_code']
    for column in uppercase_columns:
        event_w_to_date = event_w_to_date.withColumn(column, SqlFuncs.upper(event_w_to_date[column]))
    #Split columns in numeric and text values
    numeric_pattern = "^[0-9]+$"
    text_pattern = "^[^0-9]+$"
    for column in ['actor_1_geo_feature_id','actor_2_geo_feature_id']:
        event_w_to_date = event_w_to_date.withColumn(f"{column}_num", SqlFuncs.regexp_extract(SqlFuncs.col(column), numeric_pattern, 0)) \
                                        .withColumn(f"{column}_text", SqlFuncs.regexp_extract(SqlFuncs.col(column), text_pattern, 0))
    #Remove epmty strings
    df_null_replaced = event_w_to_date.na.replace("", None)
    
    no_duplicates = df_null_replaced.dropDuplicates()
    gc.collect
    no_duplicates.printSchema()
    no_duplicates_dynamic_frame = DynamicFrame.fromDF(no_duplicates, glueContext, "no_duplicates_dynamic_frame")
    return no_duplicates_dynamic_frame
        

transformed_df = cleaned_to_parquet(events)

# Script generated for node Amazon S3
AmazonS3_node1723758887267 = glueContext.getSink(path=f"s3://{S3_BUCKET_NAME}/parquet/events/", connection_type="s3",  partitionKeys=["date_added"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1723758887267")
AmazonS3_node1723758887267.setFormat("glueparquet", compression="snappy")
AmazonS3_node1723758887267.writeFrame(transformed_df)
job.commit()