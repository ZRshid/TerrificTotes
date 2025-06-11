# ----------------
# Lambda transform
# ----------------

# Zips the transform handler file for Lambda deployment.
data "archive_file" "zip_transform_handler" {
  type = "zip"
  # source_file = "${path.module}/../python/src/transform/transform_handler.py"
  #source directory of the files needed:
  source_dir = "${path.root}/../python"
  output_path = "${path.module}/zips/transform_handler.zip"
  excludes = [
    "transform/*",
    "load/*",
    "tests/*",
    "*/__pycache__",
    "__pycache__",
    ".pytest_cache"
  ]
}

# Zips the transform handler file for Lambda deployment.
data "archive_file" "pandas_layer" {
  type        = "zip"
  source_dir  = "${path.root}/transform_package/"
  output_path = "${path.root}/zips/pandas-package.zip"
}

# Uploads the ZIP file to the designated S3 bucket.
resource "aws_s3_object" "transform_lambda_code" {
  bucket = aws_s3_bucket.zip_bucket.bucket
  key    = var.transform_zip
  source = data.archive_file.zip_transform_handler.output_path
  etag = filemd5(data.archive_file.zip_transform_handler.output_path)
}

# Uploads the ZIP file to the designated S3 bucket.
resource "aws_s3_object" "transform_layer" {
  bucket = aws_s3_bucket.zip_bucket.bucket
  key    = "pandas-package.zip"
  source = data.archive_file.pandas_layer.output_path
  etag = filemd5(data.archive_file.pandas_layer.output_path)
}

#create a layer for the pandas dependencies
resource "aws_lambda_layer_version" "transform_layer_version" {
  s3_key = aws_s3_object.transform_layer.key
  s3_bucket = aws_s3_object.transform_layer.bucket
  layer_name       = "lambda_pandas_package"
  source_code_hash = "${filebase64sha256(data.archive_file.pandas_layer.output_path)}"
  depends_on = [ aws_s3_object.transform_layer ]
}

# Create the lambda function with the transform handler python file
# Links the function to an IAM role for execution permissions and sets environment variables.

resource "aws_lambda_function" "transform_handler" {
  function_name = var.transform_lambda_name
  description   = "transforms data"
  role          = aws_iam_role.lambda_role.arn
  handler       = "src.transform.initial_transform_handler.lambda_handler"
  runtime       = "python3.13"
  timeout       = 30

  depends_on = [
    data.archive_file.zip_transform_handler,
    aws_s3_bucket.zip_bucket,
    aws_s3_object.transform_layer
  ]

  s3_bucket        = aws_s3_object.transform_lambda_code.bucket
  s3_key           = aws_s3_object.transform_lambda_code.key
  source_code_hash = aws_s3_object.transform_lambda_code.etag

  layers = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python313:2"]
}
