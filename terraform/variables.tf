
variable "default_tag" {
  type        = string
  description = "default tag"
  default     = "datathon_2024_voyager"
  sensitive   = false

}

variable "region" {
  type        = string
  description = "region"
  sensitive   = false
  default     = "us-east-1"
}

variable "bucket_name" {
  type        = string
  description = "bucket_name"
  sensitive   = false
  default     = "factored-datathon-2024-voyager"
}

variable "ingest_data_s3_script_key" {
  default = "scripts/ingest_data.py"
}

variable "transform_events_script_key" {
  default = "scripts/transform_events.py"
}

variable "transform_gkgcounts_script_key" {
  default = "scripts/transform_gkgcounts.py"
}


variable "REDSHIFT_PASSWORD" {
  type        = string
  description = "database password"
  sensitive   = true
}

variable "REDSHIFT_USERNAME" {
  type        = string
  description = "database user"
  sensitive   = false
}