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