# Zips the extract handler file for Lambda deployment.
data "archive_file" "zip_extract_handler" {
  type        = "zip"
  source_file = "${path.module}/../python/src/extract/extract_handler.py"
  output_path = "${path.module}/zips/extract_handler.zip"
}

# Uploads the ZIP file to the designated S3 bucket.
resource "aws_s3_object" "extract_lambda_code" {
  bucket = aws_s3_bucket.zip_bucket.bucket
  key    = var.extract_zip
  source = data.archive_file.zip_extract_handler.output_path
}

# Create the lambda function with the extract handler python file
# Links the function to an IAM role for execution permissions and sets environment variables.

resource "aws_lambda_function" "extract_handler" {
  function_name = var.lambda_name
  description   = "extracts data"
  role          = aws_iam_role.lambda_role.arn
  handler       = "extract_handler.lambda_handler"
  runtime       = "python3.13"
  depends_on = [ data.archive_file.zip_extract_handler, aws_s3_bucket.zip_bucket ]

  s3_bucket        = var.zip_bucket
  s3_key           = var.extract_zip
  source_code_hash = filebase64sha256(data.archive_file.zip_extract_handler.output_path)

  environment {
    variables = {
      BUCKET_NAME = var.zip_bucket
    }
  }
}
