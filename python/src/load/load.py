from pyarrow import fs
import pyarrow.parquet as pq
import pg8000
import boto3
import io
import logging
from python.utils.utils import get_secret



secrets = get_secret("WarehouseSecrets")

def download_parquet_from_s3(bucket: str, key: str):
    try:
        s3 = boto3.client("s3")
        obj = s3.get_object(Bucket=bucket, Key=key)
        buffer = io.BytesIO(obj['Body'].read())  #in memory, not on disk
        return buffer
    except Exception as err:
        logging.error(f"error: {err}")
        raise 
   
def convert_buffer_to_dataframe(buffer: io.BytesIO):
    table = pq.read_table(buffer) #reads files. Bytes Io makes the data behave like a file hence it can be used here. 
    df = table.to_pandas()
    return df

# def connect_to_postgres(secrets: dict):
#     conn=pg8000.connect(
#         user = secrets["username"]
#         password = secrets["password"]
#         host = secrets["host"]
#         database = secrets["dbname"]
#         port = int(secrets["port"])  
# )
#     return conn

# def load_dataframe_to_warehouse(conn, df ):



    # for index,row in df.iterrows():
    # data = (
        
    #     row['order_id'], 
    #     row['order_date'], 
    #     row['ship_date'], 
    #     row['customer_id'], 
    #     row['customer_name'],
    #     row['segment'], 
    #     row['city'], 
    #     row['state'], 
    #     row['region'], 
    #     row['category'], 
    #     row['sales']
    
    # )


    
    # cursor.execute("""
                    
    # INSERT INTO sales(
    #         order_id, order_date, ship_date, customer_id, customer_name, 
    #         segment, city, state, region, category, sales ) 
    #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)








   








