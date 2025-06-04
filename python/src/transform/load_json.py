import awswrangler as wr
import pandas as pd
import logging
import boto3
import json


def load_json(bucket: str, key: str,table:str,s3) -> pd.DataFrame:
    """Load a JSON file from s3.

    The file must contain a first level key equal to table.


    Args:
        bucket (str): The s3 bucket.
        key (str): The files key, including path.
        table (str): The table it is loading from.
        s3: A boto3 3s client.

    Raises:
        e: ClientErrors and others

    Returns:
        pd.DataFrame: a DataFrame with all the columns from the tables JSON.
    """    
    
    try:
        # path = f"s3://{bucket}/{key}"
        # result = wr.s3.read_json([path],boto3_session= boto3_session)
        # return result
        object = s3.get_object(Bucket = bucket,Key = key)
        content= object.get('Body').read().decode('utf-8')
        data = json.loads(content)
        
        df=pd.DataFrame(data[table])
        return df
    except Exception as e:
        logging.error(msg=f"Load_json failed: '{e}'. For bucket: {bucket} and key: {key}")
        raise e