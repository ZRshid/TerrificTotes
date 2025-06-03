# Creates an S3 bucket for storing raw data extracted from the source.
resource "aws_s3_bucket" "raw_data_bucket" {
  bucket = var.raw_data_bucket
  force_destroy = true

  tags = {
    Name = "tt_raw_data_bucket"
    Environment = "Dev"
  }
}

# Enables versioning on the raw data bucket to preserve, retrieve, and restore every version of every object stored in the bucket.
resource "aws_s3_bucket_versioning" "TT_raw_data_versioning" {
  # Enable versioning for the TT Terraform state bucket
  bucket = aws_s3_bucket.raw_data_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Creates an S3 bucket for storing Lambda ZIP deployment files.
resource "aws_s3_bucket" "zip_bucket" {
  bucket = var.zip_bucket
  force_destroy = true
  tags = {
    Name = "tt_zip_bucket"
    Environment = "Dev"
  }
}

# Adds versioning configuration to the Lambda ZIP bucket - currently disabled. 
resource "aws_s3_bucket_versioning" "tt_zip_bucket_versioning" {
  # Enable versioning for the TT Terraform state bucket
  bucket = aws_s3_bucket.zip_bucket.id
  versioning_configuration {
    status = "Disabled"
  }
}

###################### ADDED 
# Creates an S3 bucket for storing processed data after being converted to parquet format.
resource "aws_s3_bucket" "processed_data_bucket" {
  bucket = var.processed_data_bucket
  force_destroy = true
  tags = {
    Name = "tt_processed_data_bucket"
    Environment = "Dev"
  }
}
##### I HAVE LEFT THIS ACTIVE
# Adds versioning configuration to the processed_data bucket 
resource "aws_s3_bucket_versioning" "tt_procesed_data_versioning" {
  # Enable versioning for the TT Terraform state bucket
  bucket = aws_s3_bucket.processed_data_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}
