variable "aws_region" {
  description = "the aws region to deploy in"
  default     = "eu-west-2"
}

variable "aws_s3_bucket" {
  description = "the backend bucket: TerrificTotes-tfstate"
  type        = string
  default     = "terrifictotes-tfstate"
}