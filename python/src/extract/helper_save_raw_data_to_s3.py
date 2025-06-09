import boto3
import logging

from datetime import datetime, timezone

def save_raw_data_to_s3(raw_data:str, table_name:str, bucket_name:str,timestamp:str|None=None):
    """
    Saves raw data to an S3 bucket with a timestamped folder structure.
    Args:
        raw_data (str): The raw data to be saved, in JSON string format.
        table_name (str): The name of the table for which the data is being saved.
        bucket_name (str): The name of the S3 bucket where the data will be stored.
        timestamp (str|None): The timestamp for the s3 bucket. In the format "%Y-%m-%d_%H:%M:%S"
    Returns:
        None
    Raises:
        Exception: If there is an error during the S3 upload.
    """
    if not isinstance(raw_data, str):
        logging.error("Raw_data must be a JSON-formatted string")
        raise TypeError("Raw_data must be a JSON-formatted string")
    if timestamp == None:
        utc_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S")
    else:
        utc_timestamp = timestamp
    s3 = boto3.client("s3", region_name='eu-west-2')
    try:
        ts_no_seconds = utc_timestamp[0:16]
        key = f"{ts_no_seconds}/{table_name}:{utc_timestamp}.json"
        s3.put_object(
            Bucket = bucket_name,
            Body = raw_data, # json string
            Key = key,
            ContentType='application/json'
        )
        logging.info(f"{key} uploaded to S3")
    except Exception as e:
        logging.error(f"Error uploading to S3: {e}")
        raise e
