# -------------------------
# Lambda IAM Role - TRANSFORM
# -------------------------
# Defines a trust policy that allows AWS Lambda to assume this role.

data "aws_iam_policy_document" "assume_role_lambda_pd" {
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
resource "aws_iam_role" "transform_role" {
  name               = "transform_roll"
  assume_role_policy = data.aws_iam_policy_document.assume_role_lambda_pd.json
}

data "aws_iam_policy_document" "s3_transform_access" {
  # IAM policy document for S3 access
  version = "2012-10-17"

  statement {
    effect = "Allow"
    actions = ["s3:ListBucket","s3:PutObject","s3:*"]
    resources = [
      # S3 bucket ARNs
      # Bucket names globally unique
      "arn:aws:s3:::${var.raw_data_bucket}",
      "arn:aws:s3:::${var.backend_bucket}",
      "arn:aws:s3:::${var.zip_bucket}"
      
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:PutObjectVersionAcl",
      "s3:*"
      # "s3:DeleteObject" revisit permission later
    ]
    resources = [
      "arn:aws:s3:::${var.backend_bucket}/*",
      "arn:aws:s3:::${var.raw_data_bucket}/*",
      "arn:aws:s3:::${var.raw_data_bucket}/*/*",
      "arn:aws:s3:::${var.zip_bucket}/*",
      "arn:aws:s3:::*"
    ]
  }
}
# Creates the actual IAM policy using the above document.
# Generic policy for lambdas
resource "aws_iam_policy" "s3_transform_access_policy" {
  name   = "s3-access-policy-transform-lambda"
  policy = data.aws_iam_policy_document.s3_transform_access.json
}

# Attaches the S3 access policy to the Lambda's IAM role.
resource "aws_iam_role_policy_attachment" "lambda_transform_access_policy_attachment" {
    role = aws_iam_role.transform_role.name
    policy_arn = aws_iam_policy.s3_transform_access_policy.arn
}

##### TRANSFORM CLOUDWATCH
#Attach cloudwatch policy to the transform role
resource "aws_iam_role_policy_attachment" "transform_cw_policy_attach" {
  role       = aws_iam_role.transform_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}