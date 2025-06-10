# Name of the S3 bucket used for storing raw data extracted from the source database.
variable "raw_data_bucket" {
  description = "raw data bucket: TerrificTotes"
  type        = string
  default     = "tt-raw-data"
}

# Name of the S3 bucket used to store the Terraform state file.
variable "backend_bucket" {
  description = "the backend bucket: TerrificTotes-tfstate"
  type        = string
  default     = "snacks-tt-tfstate"
}

# Name of the S3 bucket used for storing processed data from the raw_data bucket.
variable "processed_data_bucket" {
  description = "processed data bucket: TerrificTotes-tfstate"
  type        = string
  default     = "tt-processed-data"
}

###### Lambda Variables ######

# Name assigned to the AWS Lambda function that performs data extraction.
# Used when defining or referencing the Lambda resource.
variable "lambda_name" {
  description = "lambda handler name"
  type        = string
  default     = "extract_data_from_table"
}

# Name assigned to the AWS Lambda function that performs data transformation.
# Used when defining or referencing the Lambda resource.
variable "transform_lambda_name" {
  description = "lambda transform handler name"
  type        = string
  default     = "transform_data"
}

# Name assigned to the AWS Lambda function that performs data load to the star table.
# Used when defining or referencing the Lambda resource.
variable "load_lambda_name" {
  description = "lambda load handler name"
  type        = string
  default     = "load_data_to_warehouse"
}

# S3 bucket name where Lambda deployment packages (ZIP files) are stored.
variable "zip_bucket" {
  description = "bucket storage for zip files"
  type        = string
  default     = "tt-zip-bucket"
}

# File name of the ZIP archive containing the Lambda function code for data extraction.
variable "extract_zip" {
  description = "the zip file of extract handler lambda"
  type        = string
  default     = "extract_handler.zip"
}

# File name of the ZIP archive containing the Lambda function code for data transform.
variable "transform_zip" {
  description = "the zip file of transform handler lambda"
  type        = string
  default     = "transform_handler.zip"
}

# File name of the ZIP archive containing the Lambda function code for data load.
variable "load_zip" {
  description = "the zip file of load handler lambda"
  type        = string
  default     = "load_handler.zip"
}

###### CloudWatch Variables ######

# Variable evaluation periods
variable "evaluation_periods" {
  description = "number of evaluation periods for the cloudwatch alarm"
  type        = number
  default     = 1
}
variable "period" {
  description = "Checks every 30 seconds for new data "
  type        = number
  default     = 30
}
variable "threshold" {
  description = "Alarm will be triggered if there are 1 or more errors"
  type        = number
  default     = 1
}
variable "endpoint" {
  description = "Email for SNS"
  type        = string
  default     = "ncproject.phase@gmail.com"
}
