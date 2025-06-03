# S3 IAM 
# lambda IAM
# CloudWatch IAM
# EventBridge IAM
# SNS IAM

# ---------------
# Lambda IAM Role
# ---------------


# Defines a trust policy that allows AWS Lambda to assume this role.

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

# Creates an IAM role for the Lambda function using the trust policy defined above.
resource "aws_iam_role" "lambda_role" {
  name               = var.lambda_name
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}


# ------------------------------
# Lambda IAM Policy for S3 Read/Write
# ------------------------------

# Defines a policy that allows the Lambda function to interact with specified S3 buckets.
# Includes permission to list the buckets and read/write objects. Delete is also included but commented it out for the moment. 

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
      "arn:aws:s3:::${var.zip_bucket}"
      
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject" # revisit permission later
    ]
    resources = [
      "arn:aws:s3:::${var.backend_bucket}/*",
      "arn:aws:s3:::${var.raw_data_bucket}/*",
      "arn:aws:s3:::${var.zip_bucket}/*"
    ]
  }
}

# Creates the actual IAM policy using the above document.
# Generic policy for lambdas
resource "aws_iam_policy" "s3_access_policy" {
  name   = "s3-access-policy-lambda"
  policy = data.aws_iam_policy_document.s3_access.json
}

# Attaches the S3 access policy to the Lambda's IAM role.
resource "aws_iam_role_policy_attachment" "lambda_access_policy_attachment" {
    role = aws_iam_role.lambda_role.name # lambda_role to be changed for each lambda
    policy_arn = aws_iam_policy.s3_access_policy.arn
}

# ------------------------------
# Resource AWS Secrets Manager 
# ------------------------------

# Retrieves the existing secret in AWS Secrets Manager used by the Lambda.
data "aws_secretsmanager_secret" "aws_secret" {
  name = "totesys_secret" # secret name
}
 
# ------------------------------
# Lambda IAM Policy for Secrets Manager 
# ------------------------------


# Defines a policy that allows the Lambda to retrieve the secret value.
resource "aws_iam_policy" "lambda_secret_access" {
  name = "LambdaSecretAccessPolicy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue"
        ],
# remove when tested        Resource = "${data.aws_secretsmanager_secret.aws_secret.arn}/*"
        Resource = data.aws_secretsmanager_secret.aws_secret.arn
      } 
    ]
  })
}

# Attaches the Secrets Manager policy to the Lambda's IAM role.
# We are using the generic lambda role here, please substitute with the correct one. 

resource "aws_iam_role_policy_attachment" "attach_lambda_secret_policy" {
  role       = aws_iam_role.lambda_role.name  
  policy_arn = aws_iam_policy.lambda_secret_access.arn
}

# ------------------------------
# Lambda IAM Policy for CloudWatch
# ------------------------------

# Defines a policy document allowing the Lambda to create and write to CloudWatch Logs.
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
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/*"]
  }
}

# Creates a CloudWatch IAM policy from the above document. 
resource "aws_iam_policy" "cw_policy" {
  # use the policy document defined above
  name = "lambda-cw-policy" 
  description = "Policy for CloudWatch Logs permissions for Lambda function"
  policy = data.aws_iam_policy_document.cw_document.json
}

# Attaches the CloudWatch logging policy to the Lambda's IAM role.
resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  # attach the cw policy to the lambda role
  # edit when more lambdas will be added 
  role = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}

