import awswrangler as wr
import pandas as pd
import logging

def load_json(bucket: str, key: str) -> pd.DataFrame:
    try:
        path = f"s3://{bucket}/{key}"
        result = wr.s3.read_json([path])
        return result
    except Exception as e:
        logging.error(msg=f"load json fail {e} in bucket: {bucket} and key: {key}")
        raise e