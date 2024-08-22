resource "aws_glue_job" "ingest_data" {
  name        = "ingest_data"
  role_arn    = aws_iam_role.glue_role.arn
  description = "will get event and gkg_count files from GDELT Site"
#   max_retries = 1
  command {
    script_location = "s3://${var.bucket_name}/${var.ingest_data_s3_script_key}"
    name = "pythonshell"
    python_version = 3.9
  }
#   execution_property {
#     max_concurrent_runs = 1
#   }
  glue_version = "3.0"
}


resource "aws_glue_job" "transform_events" {
  name        = "transform_events"
  role_arn    = aws_iam_role.glue_role.arn
  description = "will transform event files from s3 and clean the data, and convert to parquet"
#   max_retries = 1
  command {
    script_location = "s3://${var.bucket_name}/${var.transform_events_script_key}"
    python_version = 3
  }
  worker_type = "G.1X"
  number_of_workers = 5
#   execution_property {
#     max_concurrent_runs = 1
#   }
  glue_version = "3.0"
  default_arguments = {
    "--job-bookmark-option"   = "job-bookmark-enable"
  }
}


resource "aws_glue_job" "transform_gkgcounts" {
  name        = "transform_gkgcounts"
  role_arn    = aws_iam_role.glue_role.arn
  description = "will transform gkg_counts files from s3 and clean the data, and convert to parquet"
#   max_retries = 1
  command {
    script_location = "s3://${var.bucket_name}/${var.transform_gkgcounts_script_key}"
    python_version = 3
  }
  worker_type = "G.1X"
  number_of_workers = 5
  
#   execution_property {
#     max_concurrent_runs = 1
#   }
  glue_version = "3.0"
  default_arguments = {
    "--job-bookmark-option"   = "job-bookmark-enable"
  }
}
