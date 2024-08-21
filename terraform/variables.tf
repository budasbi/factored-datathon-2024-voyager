
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
