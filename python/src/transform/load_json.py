import awswrangler as wr
import pandas as pd
import logging
import json


def load_json(bucket: str, key: str, table: str, s3) -> pd.DataFrame:
    """Load a JSON file from s3.

    The file must contain a first level key equal to table.


    Args:
        bucket (str): The s3 bucket.
        key (str): The files key, including path.
        table (str): The table it is loading from.
        s3: A boto3 s3 client.

    Raises:
        e: ClientErrors and others.

    Returns:
        pd.DataFrame: A DataFrame with all the columns from the tables JSON.
    """

    try:
        object = s3.get_object(Bucket=bucket, Key=key)
        content = object.get("Body").read().decode("utf-8")
        print(content, 'content')
        data = json.loads(content)
        print(data, 'data')
        df = pd.DataFrame(data[table])
        return df
    except Exception as e:
        logging.error(
            msg=f"Load_json failed: '{e}'. For bucket: {bucket} and key: {key}"
        )
        raise e
