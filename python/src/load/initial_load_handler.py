import logging
from src.load.load import (
    download_parquet_from_s3_and_saves_it_in_memory,
    convert_buffer_to_dataframe,
)
from src.transform.initial_transform_handler import make_key
from utils.utils import get_secret
from src.load.load_to_db import load_to_db

# event = {"transformed_tables", "timestamp": }
logging.getLogger().setLevel(logging.INFO)
BUCKET = "tt-processed-data"
SECRET_NAME = "WarehouseSecrets"


def lambda_handler(event, context):
    """Insert a list of tables in parquet files to their equivelent tables in the database

    Args:
        event (dict): Incoming data
        context (dict): AWS Lambda context

    Returns:
        : Returns a dictionary containing the timestamp, and table name, in the following format:
        tables':[
             {'name': 'table_name' e.g dim_staff
              'inserted_rows': 0
              }
         ]
         'timestamp':'string timestamp'}
    """
    table_names = event["tables"]
    timestamp = event["timestamp"]
    inserted_tables = []
    try:
        # {username, password,engine,host,port,dbname}
        secrets = get_secret(SECRET_NAME)

        for table_name in table_names:

            inserted_rows = insert_parquet_file_to_db(timestamp, secrets, table_name)

            result = {"name": table_name, "inserted_rows": inserted_rows}
            inserted_tables.append(result)
    except Exception as e:
        logging.error(f"Inserting Failed {e}")
        raise e
    return {"timestamp": event["timestamp"], "tables": inserted_tables}


def insert_parquet_file_to_db(timestamp, secrets, table_name):
    key = make_parquet_key(BUCKET, table_name, timestamp)
    buffer = download_parquet_from_s3_and_saves_it_in_memory(BUCKET, key)
    df_table = convert_buffer_to_dataframe(buffer)

    inserted_rows = load_to_db(
        df_table,
        table_name,
        secrets["username"],
        secrets["password"],
        secrets["host"],
        secrets["dbname"],
    )
    return inserted_rows


def make_parquet_key(bucket, table, utc_timestamp):
    return f"s3://{bucket}/{table}/{utc_timestamp}.parquet"
