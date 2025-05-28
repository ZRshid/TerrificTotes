resource "aws_s3_bucket" "tt_backend_bucket" {
  bucket = var.aws_s3_bucket
  force_destroy = true

  tags = {
    Name = "tt_backend_bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "TT_tfstate_versioning" {
  # Enable versioning for the TT Terraform state bucket
  bucket = aws_s3_bucket.tt_backend_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}