import boto3
from datetime import datetime, timezone

def save_raw_data_to_s3(raw_data:str, table_name:str, bucket_name:str):
    """
    Saves raw data to an S3 bucket with a timestamped folder structure.
    Args:
        raw_data (str): The raw data to be saved, in JSON string format.
        table_name (str): The name of the table for which the data is being saved.
        bucket_name (str): The name of the S3 bucket where the data will be stored.
    Returns:
        None
    Raises:
        Exception: If there is an error during the S3 upload.
    """
    utc_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S")
    s3 = boto3.client("s3", region_name='eu-west-2')
    try:
        s3.put_object(
            Bucket = bucket_name,
            Body = raw_data, # json string
            Key = f"{utc_timestamp[:-3]}/{table_name}:{utc_timestamp}.json",
            ContentType='application/json'
        )
    except Exception as e:
        logging.error(f"Error uploading to S3: {e}")
        raise e
