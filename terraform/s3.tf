resource "aws_s3_bucket" "raw_data_bucket" {
  bucket = var.raw_data_bucket
  force_destroy = true

  tags = {
    Name = "tt_raw_data_bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "TT_raw_data_versioning" {
  # Enable versioning for the TT Terraform state bucket
  bucket = aws_s3_bucket.raw_data_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}