# ----------------
# Lambda load
# ----------------

# Zips the load handler file for Lambda deployment.
data "archive_file" "zip_load_handler" {
  type = "zip"
  #source directory of the files needed:
  source_dir = "${path.root}/../python/src/load"
  output_path = "${path.module}/zips/load_handler.zip"
}

# Zips the load handler file for Lambda deployment.
data "archive_file" "pandas_layer" {
  type        = "zip"
  source_dir  = "${path.root}/load_package/python/sqlalchemy"
  output_path = "${path.root}/zips/SQLAlchemy-package.zip"
}

# Uploads the ZIP file to the designated S3 bucket.
resource "aws_s3_object" "load_lambda_code" {
  bucket = aws_s3_bucket.zip_bucket.bucket
  key    = var.load_zip
  source = data.archive_file.zip_load_handler.output_path
  etag = filemd5(data.archive_file.zip_load_handler.output_path)
}

# Uploads the ZIP file to the designated S3 bucket.
resource "aws_s3_object" "load_layer" {
  bucket = aws_s3_bucket.zip_bucket.bucket
  key    = "SQLAlchemy-package.zip"
  source = data.archive_file.pandas_layer.output_path
  etag = filemd5(data.archive_file.pandas_layer.output_path)
}

#create a layer for the pandas dependencies
resource "aws_lambda_layer_version" "load_layer_version" {
  s3_key = aws_s3_object.load_layer.key
  s3_bucket = aws_s3_object.load_layer.bucket
  layer_name       = "lambda_pandas_package"
  source_code_hash = "${filebase64sha256(data.archive_file.pandas_layer.output_path)}"
  depends_on = [ aws_s3_object.load_layer ]
}

# Create the lambda function with the load handler python file
# Links the function to an IAM role for execution permissions and sets environment variables.

resource "aws_lambda_function" "load_handler" {
  function_name = var.load_lambda_name
  description   = "loads data"
  role          = aws_iam_role.lambda_role.arn
  handler       = "src.load.initial_transform_handler.lambda_handler" ##PUT THE FILENAME HERE
  runtime       = "python3.13"
  timeout       = 30

  depends_on = [
    data.archive_file.zip_load_handler,
    aws_s3_bucket.zip_bucket,
    aws_s3_object.load_layer
  ]

  s3_bucket        = aws_s3_object.load_lambda_code.bucket
  s3_key           = aws_s3_object.load_lambda_code.key
  source_code_hash = aws_s3_object.load_lambda_code.etag

  layers = [aws_lambda_layer_version.load_layer_version.arn]
}
