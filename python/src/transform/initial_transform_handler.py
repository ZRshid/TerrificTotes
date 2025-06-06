import logging
import boto3
from src.transform.load_json import load_json
from src.transform.to_parquet import to_parquet
from src.transform.transform_counterparty import transform_counterparty
from src.transform.transform_design import transform_design
from src.transform.transform_location import transform_location
from src.transform.transform_payment_type import transform_payment_type
from src.transform.transform_staff import transform_staff_with_department
from src.transform.transform_transaction import transform_transaction
from src.transform.dim_date import dim_date
from src.transform.load_currency import load_currency_codes_from_s3
#import fact tables

#this can set any level of that the message actually appears 
#otherwise its default is none which doesnt log it
logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context):
    

    """
    setup event, client, response
    load json file from raw data bucket
    transform data
    convert transform data to parquet format
    load transformed data to processed bucket

    returns a dict list of all uploaded tables: {"tables": [list of tables]}
    """
    s3 = boto3.client("s3")
    transformed_tables = []
    raw_bucket = "tt-raw-data"
    processed_bucket = "tt-processed-data"  #hard coded for now
    key_address = "2025-06-03_08:08/address:2025-06-03_08:08:57.json"
    key_counterparty = "2025-06-03_08:08/counterparty:2025-06-03_08:08:45.json"
    key_design = "2025-06-03_08:08/design:2025-06-03_08:08:48.json"
    df_address = None

#order to write function: staff, payment_types, transaction, date, currency

    dim_location = location(event, s3, transformed_tables, raw_bucket, key_address)
    dim_design = design(event, s3, transformed_tables, raw_bucket, key_design)
    dim_counterparty = counterparty(event, s3, transformed_tables, raw_bucket, key_address, key_counterparty, df_address)

    print(transformed_tables)
    return {"transformed_tables": transformed_tables}

def counterparty(event, s3, transformed_tables, raw_bucket, key_address, key_counterparty, df_address):
    if "counterparty" in event["tables"]:
        try:
            df_counterparty = load_json(raw_bucket, key_counterparty, "counterparty", s3)
            if df_address is None:
                df_address = load_json(raw_bucket, key_address, "address", s3)
            transformed_counterparty = transform_counterparty(df_counterparty, df_address)
            print(transformed_counterparty.to_string())
            # to_parquet(transformed_counterparty, processed_bucket, "key")
            transformed_tables.append("dim_counterparty")
            return transformed_counterparty
        except Exception as e:
            logging.error(f"Failed to process counterparty: {e}")

def location(event, s3, transformed_tables, raw_bucket, key_address):
    if "address" in event["tables"]:
        try:
            df_address = load_json(raw_bucket, key_address, "address", s3)
            transformed_address = transform_location(df_address)
            transformed_tables.append("dim_location")
            return transformed_address
        except Exception as e:
            logging.error(f"Failed to process address: {e}")
            raise e
        
def design(event, s3, transformed_tables, raw_bucket, key_address):
    if "design" in event["tables"]:
        try:
            df_design = load_json(raw_bucket, key_address, "design", s3)
            transformed_design = transform_design(df_design)
            # to_parquet(transformed_design, processed_bucket, "key")
            transformed_tables.append("dim_design")
            return transformed_design
        except Exception as e:
            logging.error(f"Failed to process address: {e}")




if __name__ == "__main__":
    event = {"tables" : ["counterparty", "currency", "department", "design", "staff", "sales_order", 
                "address", "payment", "purchase_order", "payment_type", "transaction"]}
    lambda_handler(event, {})