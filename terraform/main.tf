terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    # Storing Terraform state on S3 for remote access
    bucket = "snacks-tt-tfstate" # Variables are not supported in backend config
    key = "terraform.tfstate"
    region = "eu-west-2"
  }
}

# Configure the AWS provider 
provider "aws" {
  region = "eu-west-2"
}