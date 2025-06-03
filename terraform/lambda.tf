# Zips the extract handler file for Lambda deployment.
data "archive_file" "zip_extract_handler" {
  type        = "zip"
  # source_file = "${path.module}/../python/src/extract/extract_handler.py"
    source_dir = "${path.root}/../python"
    excludes = [
    "transform/*",
    "load/*",
    "tests/*",
    "*/__pycache__",
    "*/*/__pycache__",
    ".pytest_cache"
  ]
  output_path = "${path.module}/zips/extract_handler.zip"
}

data "archive_file" "pg8000_layer" {
  type        = "zip"
  source_dir  = "${path.root}/package/"
  output_path = "${path.root}/zips/package.zip"
}

# Uploads the ZIP file to the designated S3 bucket.
resource "aws_s3_object" "extract_lambda_code" {
  bucket = aws_s3_bucket.zip_bucket.bucket
  key    = var.extract_zip
  source = data.archive_file.zip_extract_handler.output_path
}

# Uploads the ZIP file to the designated S3 bucket.
resource "aws_s3_object" "extract_lambda_layer" {
  bucket = aws_s3_bucket.zip_bucket.bucket
  key    = "package.zip"
  source = data.archive_file.zip_extract_handler.output_path
}

resource "aws_lambda_layer_version" "lambda_package_layer" {
  filename   = data.archive_file.pg8000_layer.output_path
  layer_name = "lambda_python_package"
  source_code_hash = data.archive_file.pg8000_layer.output_base64sha256
}

# Create the lambda function with the extract handler python file
# Links the function to an IAM role for execution permissions and sets environment variables.

resource "aws_lambda_function" "extract_handler" {
  function_name = var.lambda_name
  description   = "extracts data"
  role          = aws_iam_role.lambda_role.arn
  handler       = "src.extract.extract_handler.lambda_handler"
  runtime       = "python3.13"
  depends_on = [ data.archive_file.zip_extract_handler, 
                aws_s3_bucket.zip_bucket,
                aws_s3_object.extract_lambda_layer 
                ]

  s3_bucket        = aws_s3_object.extract_lambda_code.bucket
  s3_key           = aws_s3_object.extract_lambda_code.key
  source_code_hash = filebase64sha256(data.archive_file.zip_extract_handler.output_path) #aws_s3_object.extract_lambda_code.etag #

  layers = [aws_lambda_layer_version.lambda_package_layer.arn]

  publish = true
  environment {
    variables = {
      BUCKET_NAME = var.zip_bucket
    }
  }
}
