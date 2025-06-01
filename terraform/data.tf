
# Retrieves the AWS caller identity of the credentials being used.
data "aws_caller_identity" "current" {}

# Retrieves the AWS region configuration in use.
data "aws_region" "current" {}