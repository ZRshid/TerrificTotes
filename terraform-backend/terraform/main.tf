provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project = "Final_Project"
      Env     = "Dev"
      Owner   = "Culinary"
      Backend = "Holds_tfstate"
    }
  }
}