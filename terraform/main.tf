terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.54.0"
    }
  }
  required_version = "~> 1.8"
}

provider "aws" {
  region = "us-east-1"
}