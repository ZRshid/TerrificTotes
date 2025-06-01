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

# Name assigned to the AWS Lambda function that performs data extraction.
# Used when defining or referencing the Lambda resource.
variable "lambda_name" {
  description = "lambda handler name"
  type        = string
  default     = "extract_data_from_table"
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