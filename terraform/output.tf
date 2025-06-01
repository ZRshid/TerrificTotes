
# Outputs the absolute local file path to the "zips" directory within the current Terraform module.
output "zip_path" {
  value = "${path.module}/zips"
}