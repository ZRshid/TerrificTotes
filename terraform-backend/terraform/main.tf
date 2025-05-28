provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project = "Final_Project"
      Env     = "Dev"
      Owner   = "Snacks"
      Backend = "Holds_tfstate"
    }
  }
}
