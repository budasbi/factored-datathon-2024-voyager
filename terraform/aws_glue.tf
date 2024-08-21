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