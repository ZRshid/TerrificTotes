from pyarrow import fs
import pyarrow.parquet as pq
import boto3
import io
import logging
from python.utils.utils import get_secret

secrets = get_secret("WarehouseSecrets")

def download_parquet_from_s3_and_saves_it_in_memory(bucket: str, key: str) -> str:
    """
    Downloads data from an S3 bucket in parquet format. 
    Args:
        bucket (str): The s3 bucket where the data is stored in.
        key (str): This is the S3 key, it contains the path within the bucket where the files are stored.
    Returns:
        A Buffer: Essentialy stores the files in memory and not on disk.
    Raises:
        Exception: If there is an exception when downloading the files and saving it in memory, an exception is raised.
    """
    try:
        s3 = boto3.client("s3")
        obj = s3.get_object(Bucket=bucket, Key=key)
        buffer = io.BytesIO(obj['Body'].read())  #in memory, not on disk
        return buffer
    except Exception as err:
        logging.error(f"error: {err}")
        raise err
   
def convert_buffer_to_dataframe(buffer: io.BytesIO) -> io.BytesIO:
    """
    Downloads the buffer (data stored in memory) to a dataframe. 
    Args:
        buffer: This is the data stored in memory. 
    Returns:
         A Dataframe.   
    Raises:
         Exception: If there is an exception when converting the files into a dataframe, an exception is raised. 
    """
    try:
        table = pq.read_table(buffer) #reads files. Bytes Io makes the data behave like a file hence it can be used here. 
        df = table.to_pandas()
        return df
    except Exception as err:
        logging.error(f"error: The file could not be  {err}")
        raise err
                      

   