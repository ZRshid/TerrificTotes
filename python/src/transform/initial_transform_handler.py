import logging
import boto3
import pandas as pd
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
from datetime import datetime
#import fact tables

#this can set any level of that the message actually appears 
#otherwise its default is none which doesnt log it
logging.getLogger().setLevel(logging.INFO)

INITIAL_DATE = datetime(2022,1,1)
FUTURE_DATE =datetime(2025,12,31)
RAW_DATA_BUCKET = "tt-raw-data"

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
    transformed_tables = {} #dictionart to contain the transformed dataframes
    
    processed_bucket = "tt-processed-data"  #hard coded for now
    timestamp = event.get("timestamp",datetime.now.strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3])
    key_address = "2025-06-03_08:08/address:2025-06-03_08:08:57.json"
    key_counterparty = "2025-06-03_08:08/counterparty:2025-06-03_08:08:45.json"
    key_design = "2025-06-03_08:08/design:2025-06-03_08:08:48.json"
    df_address = None
    # replace with switch-case, default log ?
    if "address" in event["tables"]:
        transformed_tables["dim_location"] = transform_table("address", s3, RAW_DATA_BUCKET, key_address,transform_location)
    if "design" in event["tables"]:
        transformed_tables["dim_design"] = transform_table("design", s3, RAW_DATA_BUCKET, key_design,transform_design)
    if "payment_types" in event["tables"]:
        transformed_tables["dim_payment_types"] = transform_table("payment_types", s3, RAW_DATA_BUCKET, key_design,transform_payment_type)
    if "transaction" in event["tables"]:
        transformed_tables["dim_transaction"] = transform_table("transaction", s3, RAW_DATA_BUCKET, key_design,transform_transaction)
    if "currency" in event["tables"]:
        transformed_tables["dim_currency"] = load_currency_codes_from_s3(["currency_code","currency_name"])
    

    dim_counterparty = counterparty(event, s3, transformed_tables, RAW_DATA_BUCKET, key_address, key_counterparty, df_address)
    # dim_staff = 

    #uncomment when create_dates available:
    # if "date" in event["tables"]:
    #     transformed_tables["dim_dates"] = create_dates(INITIAL_DATE,FUTURE_DATE)

    #repeat for all tables:
    for table_name,df_table in transformed_tables.items():
       to_parquet(df_table, processed_bucket,table_name ,timestamp)


    return {"transformed_tables": transformed_tables.keys(),"timestamp":timestamp} 

"""todo: 
        finish loading dimensions
        TESTS - don't need to test functions from other files - have already been tested
        change extract handler to return a timestamp & file name
        make key from table name and time stamp - test
        change function to use keys and bucket dynamically
        save to parquet with correct key
"""
def make_key(table:str, timestamp:str):
   ...


#combine to use two tables 
def counterparty(event, s3, transformed_tables, raw_bucket, key_address, key_counterparty, df_address):
    if "counterparty" in event["tables"]:
        try:
            df_counterparty = load_json(raw_bucket, key_counterparty, "counterparty", s3)
            if df_address is None:
                raise ValueError("")
            
            transformed_counterparty = transform_counterparty(df_counterparty, df_address)
            
            return transformed_counterparty
        except Exception as e:
            logging.error(f"Failed to process counterparty: {e}")
            raise e

def transform_table(table_name:str, s3, raw_bucket:str, key_address:str, transform) -> pd.DataFrame:
    """load table then transform to dimension

    Args:
        table_name (str): the table
        s3 (_type_): context
        raw_bucket (str): the bucket
        key_address (str): the file
        transform (function): how to transform

    Returns:
        pd.da: a dimension dataframe
    """        
    try:
        df = load_json(raw_bucket, key_address, table_name, s3)
        transformed_df = transform(df)
        return transformed_df
    except Exception as e:
        logging.error(f"Failed to process {table_name}: {e}")
        raise e




if __name__ == "__main__":
    event = {"tables" : ["counterparty", "currency", "department", "design", "staff", "sales_order", 
                "address", "payment", "purchase_order", "payment_type", "transaction"]}
    lambda_handler(event, {})