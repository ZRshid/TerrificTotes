# TerrificTotes

## Highlights
- 

## Overview
Previously written

## Features
- Fetch data from Totesy database


## Tech Stack
- Python
- Terraform
- Lambda
- S3
- PostgreSQL
- Pandas
- pg8000
- Pytest
- CloudWatch
- Boto3
- Moto
- SQLAlchemy
- PyArrow

## Setup Instructions

### 1. Clone the repo:
```bash
git clone https://github.com/C0d3r34/TerrificTotes.git
cd TerrificTotes
```
### 2. Create a virtual environment and install dependencies:
```bash
make requirements
```
### 3. Activate the virtual environment:
```bash
source venv/bin/activate
```
### 4. Bootstrap the remote Terraform backend:
```bash
cd terraform-backend
terraform init
terraform plan
terraform apply
```
### 5. Create Terraform layers:
```bash
cd ..
make terraform-layers-requirements
```
### 6. Deploy the full infrastructure:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```
### 7. Run tests:
```bash
make run-checks
```

> Ensure your credentials are saved in secrets manager on AWS for access to the databases.

## Project Structure
```
.github/workflows/
    etl-workflow.yml

Data/
    Currency-codes.csv

python/
    src/
        extract/
            extract_handler.py
            helper_create_sql.py
            helper_json.py
            helper_query_db.py
            helper_save_raw_data_to_s3.py
        load/
            initial_load_handler.py
            load.py
            load_to_db.py
        transform/
            dim_date.py
            fact_sales.py
            helper_upload_csv_to_zip_bucket.py
            initial_transform_handler.py
            load_currency.py
            load_json.py
            to_parquet.py
            transform_counterparty.py
            transform_design.py
            transform_location.py
            transform_payment_type.py
            transform_staff.py
            transform_transaction.py
    tests/
        test_extract/
            test_connection.py
            test_extract_handler.py
            test_helper_create_sql.py
            test_helper_save_raw_data_to_s3.py
            test_to_JSON.py
        test_load/
            test_initial_load_handler.py
            test_load.py
            test_load_to_db.py
        test_transform/
            test_dim_date.py
            test_fact_sales.py
            test_helper_load_csv_to_zip_bucket.py
            test_initial_transform_handler.py
            test_load_currency.py
            test_load_json.py
            test_to_parquet.py
            test_transform_counterparty.py
            test_transform_design.py
            test_transform_location.py
            test_transform_payment.py
            test_transform_staff.py
            test_transform_transaction.py
        test_utils.py
    utils/
        utils.py 

terraform-backend/
    .terraform.lock.hcl
    main.tf
    output.tf
    s3.tf
    vars.tf
    
terraform/
    .terraform.lock.hcl
    cloudwatch.tf
    data.tf
    extract_lambda.tf
    iam.tf
    load_lambda.tf
    main.tf
    output.tf
    s3.tf
    transform_lambda.tf
    vars.tf

.gitignore
Makefile
README.md
requirements.dev.txt
requirements.txt
snacks.txt
```

## Reflections
- 