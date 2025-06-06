import logging
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
    pass

    """
    setup event, client, response
    load json file from raw data bucket
    transform data
    convert transform data to parquet format
    load transformed data to processed bucket

    returns a dict list of all uploaded tables: {"tables": [list of tables]}
    """