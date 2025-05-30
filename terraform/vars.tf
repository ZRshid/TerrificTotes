variable "raw_data_bucket" {
  description = "raw data bucket: TerrificTotes"
  type        = string
  default     = "tt-raw-data"
}

variable "backend_bucket" {
  description = "the backend bucket: TerrificTotes-tfstate"
  type        = string
  default     = "snacks-tt-tfstate"
}

variable "lambda_name" {
  description = "lambda handler name"
  type        = string
  default     = "lambda_template"
}

variable "zip_bucket" {
  description = "bucket storage for zip files"
  type        = string
  default     = "tt-zip-bucket"
}

variable "extract_zip" {
  description = "the zip file of extract handler lambda"
  type        = string
  default     = "extract_handler.zip"
}