import awswrangler as wr
import pandas as pd
import logging
from datetime import datetime, timezone

def to_parquet(df: pd.DataFrame, bucket:str, key:str):
    """
    Converts data into parquet format .
    Args:
        df(str): Dataframes stored in the bucket
        bucket (pd.DataFrame): The name of the S3 bucket where the dataframes will be stored.
        key (str): The path to the bucket for which the dataframes are being saved.
    Returns:
        None
    Raises:
        Exception: If there is an error during the S3 upload.
    """

    try:
        utc_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S")
        path = f"s3://{bucket}/{key}/{utc_timestamp}.parquet"
        wr.s3.to_parquet(df=df, path=path)
    except Exception as e:
         logging.error(msg=f"Exporting to parquet {path} in {df} and bucket: {bucket} failed")

