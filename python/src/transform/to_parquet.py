import awswrangler as wr
import pandas as pd
import logging
from datetime import datetime, timezone

def to_parquet(df: pd.DataFrame, bucket:str, key:str,timestamp:str|None = None):
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
        if timestamp==None:
            utc_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S")
        else:
            utc_timestamp = timestamp.replace(' ', '_')
        path = f"s3://{bucket}/{key}/{utc_timestamp}.parquet"
        # df.to_parquet(path)
        logging.info(f"writing parquet for {path}")
        df=pd.DataFrame({
            'col': [1, 2, 3],
            'col2': ['A', 'A', 'B'],
            'col3': [None, None, None]
        })
        import io,boto3
        s3 = boto3.client("s3")
        out_buffer = io.BytesIO()
        df.to_parquet(out_buffer, index=False)
        s3.put_object(Bucket=bucket, Key=f"/{key}/{utc_timestamp}.parquet", Body=out_buffer.getvalue())
        # wr.s3.to_parquet(df=df, path=path)
        logging.info(f"writen parquet for {path}")
    except Exception as e:
         logging.error(msg=f"Exporting to parquet failed {path} because: {e} with {df}")

