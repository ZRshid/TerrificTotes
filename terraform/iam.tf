# S3 IAM 
# lambda IAM
# CloudWatch IAM
# EventBridge IAM
# SNS IAM

# ---------------
# Lambda IAM Role
# ---------------

# Define
data "aws_iam_policy_document" "trust_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# Created for each lambda
resource "aws_iam_role" "lambda_role" {
  name               = var.lambda_name
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}


# ------------------------------
# Lambda IAM Policy for S3 Write
# ------------------------------

# Define
data "aws_iam_policy_document" "s3_access" {
  # IAM policy document for S3 access
  version = "2012-10-17"

  statement {
    effect = "Allow"
    actions = ["s3:ListBucket"]
    resources = [
      # S3 bucket ARNs
      # Bucket names globally unique
      "arn:aws:s3:::${var.backend_bucket}",
      "arn:aws:s3:::${var.raw_data_bucket}",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      # "s3:DeleteObject" revisit permission later
    ]
    resources = [
      "arn:aws:s3:::${var.backend_bucket}/*",
      "arn:aws:s3:::${var.raw_data_bucket}/*"
    ]
  }
}

# Create
# Generic policy for lambdas
resource "aws_iam_policy" "s3_access_policy" {
  name   = "s3-access-policy-lambda"
  policy = data.aws_iam_policy_document.s3_access.json
}

# Attach below to each lambda
resource "aws_iam_role_policy_attachment" "lambda_access_policy_attachment" {
    role = aws_iam_role.lambda_role.name # lambda_role to be changed for each lambda
    policy_arn = aws_iam_policy.s3_access_policy.arn
}


# ------------------------------
# Lambda IAM Policy for CloudWatch
# ------------------------------

# Define
data "aws_iam_policy_document" "cw_document" {
  statement {
    # this statement should give permission to create Log Groups in your account
    effect = "Allow"
    actions = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"]
  }

  statement {
    # this statement should give permission to create Log Streams and put Log Events in the lambda's own Log Group
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    # edit when more lambdas will be added 
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:aws/lambda/${var.lambda_name}:*"]
  }
}

# Create 
resource "aws_iam_policy" "cw_policy" {
  # use the policy document defined above
  name = "lambda-cw-policy" 
  description = "Policy for CloudWatch Logs permissions for Lambda function"
  policy = data.aws_iam_policy_document.cw_document.json
}

# Attach
resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  # attach the cw policy to the lambda role
  # edit when more lambdas will be added 
  role = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}
