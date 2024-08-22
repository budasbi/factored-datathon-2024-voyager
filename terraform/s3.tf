resource "aws_s3_bucket" "data_challenge_bucket" {
  bucket        = var.bucket_name
  force_destroy = true
  tags = {
    Name = var.default_tag
  }
}

#Deploy GLue Scripts
#Ingest Script
resource "aws_s3_object" "upload_ingest_data_script"{
    bucket = "${var.bucket_name}"
    key = var.ingest_data_s3_script_key
    source = "../scripts/glue_jobs/ingest_data.py"
    depends_on = [ aws_s3_bucket.data_challenge_bucket ]

}

resource "aws_s3_object" "upload_transform_events_script"{
    bucket = "${var.bucket_name}"
    key = var.transform_events_script_key
    source = "../scripts/glue_jobs/transform_events.py"
    depends_on = [ aws_s3_bucket.data_challenge_bucket ]

}


resource "aws_s3_object" "upload_transform_gkg_counts_script"{
    bucket = "${var.bucket_name}"
    key = var.transform_gkgcounts_script_key
    source = "../scripts/glue_jobs/transform_gkgcounts.py"
    depends_on = [ aws_s3_bucket.data_challenge_bucket ]

}