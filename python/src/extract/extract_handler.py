import logging
import json
from pprint import pprint
from python.src.extract.helper_create_sql import create_sql
from python.src.extract.helper_query_db import connect_to_db, close_db, query_db
from python.src.extract.helper_json import to_JSON 
from python.src.extract.helper_save_raw_data_to_s3 import save_raw_data_to_s3
from datetime import datetime


#this can set any level of that the message actually appears 
#otherwise its default is none which doesnt log it
logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context):
    # convert json to dict 
    event_dict = json.loads(event)
    pprint(event_dict)

    # take the table from the event list 
    table = event_dict['tables'][0]
    from_time = datetime.strptime(event_dict['from_time']) 
    to_time = datetime.strptime(event_dict['to_time']) 
    raw_data_bucket = event_dict['raw_data_bucket']

    # pass the table name and times to create SQL
    query = create_sql(table, from_time, to_time)

    # pass this SQL to query_db 
    connect_to_db()
    rows,columns = query_db(query) 
    close_db()

    # pass the tuple to json 

    table_json = to_JSON(table, from_time, to_time)

    # pass the json to save raw_data
    #save_raw_data_to_s3(raw_data:str, table_name:str, bucket_name:str): 

    save_raw_data_to_s3(raw_data= table_json, table_name = table, bucket_name = raw_data_bucket)

    # return list of tables  

    return {"tables": ["sales"]} 



