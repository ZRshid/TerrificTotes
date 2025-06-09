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
from src.transform.dim_date import create_dim_date
from src.transform.load_currency import load_currency_codes_from_s3
from src.transform.fact_sales import sales_facts
from datetime import datetime
import pytz

# import fact tables

# this can set any level of that the message actually appears
# otherwise its default is none which doesnt log it
logging.getLogger().setLevel(logging.INFO)

# TODO: Hard coded for now, maybe add to event?
INITIAL_DATE = datetime(2022, 1, 1)
FUTURE_DATE = datetime(2025, 12, 31)
RAW_DATA_BUCKET = "tt-raw-data"
PROCESSED_BUCKET = "tt-processed-data"


def lambda_handler(event, context):
    """load each table in the event, transform them, convert to parquet format, and saving to the processed bucket.

    Args:
        event (dict): The Lambda event dictionary needs 'tables' and 'timestamp' keys
        conteext (dict): The Lambda context
    Returns:
        dict: A dict list of all uploaded tables and the timestamp: {"tables": [list of tables],'timestamp':sting}
    """
    try:
        s3 = boto3.client("s3")
        transformed_tables = {}  # dictionart to contain the transformed dataframes

        # get timestamp from event or use current time
        timestamp = event.get(
            "timestamp", datetime.now(tz=pytz.UTC).strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3]
        )

        # transform tables given in the event
        transformed_tables = transform_tables(event["tables"], s3)

        # save all transformed all tables:
        for table_name, df_table in transformed_tables.items():
            to_parquet(df_table, PROCESSED_BUCKET, table_name, timestamp)
    except Exception as e:
        logging.error(f"Table transforms failed: {e}")
        raise e

    return {"transformed_tables": transformed_tables.keys(), "timestamp": timestamp}


"""todo: 
        finish loading dimensions
        TESTS - don't need to test functions from other files - have already been tested
        change extract handler to return a timestamp & file name
        make key from table name and time stamp - test
        change function to use keys and bucket dynamically
        save to parquet with correct key
"""


def make_key(table: str, timestamp: str) -> str:
    """make a key for the extracted table"""
    time = timestamp.replace(" ", "_")
    dir = time[:16]
    stamp = time[:19]
    return f"{dir}/{table}:{stamp}.json"


def transform_and_combine(
    table_name, s3, raw_bucket, key, secondary_key, seconday_table, transform_func
) -> pd.DataFrame:
    """Load two tables and transform into one dimension

    Args:
        table_name (str): the table's name
        s3 (_type_): context
        raw_bucket (str): the bucket
        key (_type_): key to main table
        secondary_key (_type_): key to secondary table
        seconday_table (_type_): the secondary table's name
        transform_func (_type_): a function used to transform the tables

    Returns:
        pd.Dataframe: a dimension dataframe
    """
    try:
        df_table = load_json(raw_bucket, key, table_name, s3)
        seconday_df = load_json(raw_bucket, secondary_key, seconday_table, s3)

        transformed_table = transform_func(df_table, seconday_df)

        return transformed_table
    except Exception as e:
        logging.error(f"Failed to process {table_name}: {e}")
        raise e


def transform_table(
    table_name: str, s3, raw_bucket: str, key_address: str, transform
) -> pd.DataFrame:
    """load table then transform to dimension

    Args:
        table_name (str): the table
        s3 (_type_): context
        raw_bucket (str): the bucket
        key_address (str): the file
        transform (function): how to transform

    Returns:
        pd.Dataframe: a dimension dataframe
    """
    try:
        df = load_json(raw_bucket, key_address, table_name, s3)
        transformed_df = transform(df)
        return transformed_df
    except Exception as e:
        logging.error(f"Failed to process {table_name}: {e}")
        raise e


def transform_tables(tables: list, s3, timestamp: str) -> dict:
    """Transform all the tables in the list (assuming they are in this fucntion)

    Args:
        tables (list): list of tables
        s3 (_type_): an S3
        timestamp (str_): When the extract happened

    Raises:
        ValueError: if one of the secondary tables is missing

    Returns:
        dict: A dictionary with name:dataframe of the transformed tables
    """

    # replace with switch-case, default log ?
    transformed_tables = {}

    # Create dataframes for dimensions
    if "address" in tables:
        key = make_key("address", timestamp)
        transformed_tables["dim_location"] = transform_table(
            "address", s3, RAW_DATA_BUCKET, key, transform_location
        )
    if "design" in tables:
        key = make_key("design", timestamp)
        transformed_tables["dim_design"] = transform_table(
            "design", s3, RAW_DATA_BUCKET, key, transform_design
        )
    if "payment_types" in tables:
        key = make_key("payment_types", timestamp)
        transformed_tables["dim_payment_types"] = transform_table(
            "payment_types", s3, RAW_DATA_BUCKET, key, transform_payment_type
        )
    if "transaction" in tables:
        key = make_key("transaction", timestamp)
        transformed_tables["dim_transaction"] = transform_table(
            "transaction", s3, RAW_DATA_BUCKET, key, transform_transaction
        )
    if "counterparty" in tables:
        if "address" in tables:
            key_counterparty = make_key("counterparty", timestamp)
            key_address = make_key("address", timestamp)
            transformed_tables["dim_counterparty"] = transform_and_combine(
                "counterparty",
                s3,
                RAW_DATA_BUCKET,
                key_counterparty,
                key_address,
                "address",
                transform_counterparty,
            )
        else:
            raise ValueError(
                "address table missing unable to transform counterparty table"
            )
    if "staff" in tables:
        if "department" in tables:
            staff_key = make_key("staff", timestamp)
            department_key = make_key("department", timestamp)
            transformed_tables["dim_staff"] = transform_and_combine(
                "staff",
                s3,
                RAW_DATA_BUCKET,
                staff_key,
                department_key,
                "department",
                transform_staff_with_department,
            )
        else:
            raise ValueError("department table missing unable to transform staff table")

    if "currency" in tables:
        key = make_key("currency", timestamp)
        transformed_tables["dim_currency"] = load_currency_codes_from_s3(
            ["currency_code", "currency_name"]
        )
    if "date" in tables:
        transformed_tables["dim_dates"] = create_dim_date(INITIAL_DATE, FUTURE_DATE)

    # dataframe for fact table
    if "sales" in tables:
        sales_key = make_key("sales", timestamp)
        transformed_tables["fact_sales_order"] = transform_table(
            "sales", s3, RAW_DATA_BUCKET, sales_key, "sales", sales_facts
        )

    return transformed_tables


if __name__ == "__main__":
    event = {
        "tables": [
            "counterparty",
            "currency",
            "department",
            "design",
            "staff",
            "sales_order",
            "address",
            "payment",
            "purchase_order",
            "payment_type",
            "transaction",
        ]
    }
    lambda_handler(event, {})
