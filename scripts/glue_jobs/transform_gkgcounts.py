import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as SqlFuncs
from awsglue.dynamicframe import DynamicFrame
import gc
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
gkgcounts = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": False, "separator": "\t", "optimizePerformance": False}, 
                                                          connection_type="s3", format="csv", connection_options={"paths": ["s3://factored-datathon-2024-voyager/raw/gkg_counts/"], 
                                                                                                                  "recurse": True}, transformation_ctx="gkgcounts")


# %%
def cleaned_to_parquet(raw_gkg_counts):
    spark_df_gkgcounts = raw_gkg_counts.toDF()
    gkg_colums=['date','numarts', 'count_type', 'number', 'object_type', 'geo_type', 'geo_fullname', 'geo_country_code', 'geo_adm1_code', 'geo_lat', 'geo_long','geo_feature_id', 'cameo_event_ids', 'sources', 'source_urls' ]
    gkg_counts_columns = spark_df_gkgcounts.toDF(*gkg_colums)
    gkg_counts_date = gkg_counts_columns.withColumn('date', SqlFuncs.to_date('date', 'yyyyMMdd'))
    #Split Cameo_event_ids
    gkg_counts_split = gkg_counts_date.withColumn("cameo_event_ids_split", SqlFuncs.split(gkg_counts_date["cameo_event_ids"], ","))
    gkg_counts_explode = gkg_counts_split.withColumn("cameo_event_ids", SqlFuncs.explode(gkg_counts_split["cameo_event_ids_split"]))
    gkg_counts_ex = gkg_counts_explode.drop("cameo_event_ids_split")
    gkg_counts_nodups = gkg_counts_ex.dropDuplicates()
    
    gc.collect()
    no_duplicates_dynamic_frame = DynamicFrame.fromDF(gkg_counts_nodups, glueContext, "no_duplicates_dynamic_frame")
    return no_duplicates_dynamic_frame
    
    
    
    

transformed_df = cleaned_to_parquet(gkgcounts)
AmazonS3_node1723758887267 = glueContext.getSink(path="s3://factored-datathon-2024-voyager/parquet/gkg_counts/", connection_type="s3",  partitionKeys=["date"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1723758887267")
AmazonS3_node1723758887267.setFormat("glueparquet", compression="snappy")
AmazonS3_node1723758887267.writeFrame(transformed_df)
job.commit()