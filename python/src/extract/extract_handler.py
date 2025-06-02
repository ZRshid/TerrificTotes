import logging
import json
from python.src.extract.helper_create_sql import create_sql
from python.src.extract.helper_query_db import connect_to_db, close_db, query_db
from python.src.extract.helper_json import to_JSON 
from python.src.extract.helper_save_raw_data_to_s3 import save_raw_data_to_s3

#this can set any level of that the message actually appears 
#otherwise its default is none which doesnt log it
logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event:dict, context:dict) -> dict:
    """ 
    A handler function to extract data from tables specified in the event,
    for the time period in the event.

    Args:
        event (dict): A dictionary with the folloing keys:
            tables: A list of table names, 
            start_time : A formated time string compatible with postgresql.
            end_time A formated time string compatible with postgresql.
        context (dict): aws context

    Returns:
        dict: A dictionary with the key tables, a list of extracted tables.
    """    
    # convert json to dict 
    event_dict = json.loads(event)

    from_time = event_dict['from_time']
    to_time = event_dict['to_time'] 
    raw_data_bucket = event_dict['raw_data_bucket']

    # take the table from the event list 
    tables = []
    try:
        conn = connect_to_db("totesys_secret")
        for table in event_dict['tables']:
            # pass the table name and times to create SQL
            query = create_sql(table, from_time, to_time)

            # pass this SQL to query_db 
            rows,columns = query_db(query, conn) 

            # pass the tuple to json 
            table_json = to_JSON(table, columns, rows ,from_time, to_time)

            # pass the json to save raw_data
            save_raw_data_to_s3(raw_data=table_json, table_name=table, bucket_name=raw_data_bucket)

            tables.append(table)
    except Exception as e:
        message = f"Extraction Failed: On table {table}, previously extracted: {tables}. {e}"
        logging.critical(message)
        raise e
    finally:
        close_db(conn)

    #assume if it gets this far it worked
    message = f"Extract Succeeded for {len(tables)} tables at {to_time} "
    logging.info(message)
    
    # return list of tables  
    return {"tables": tables} 

if __name__ == "__main__":
    event =  '''{"tables" : ["counterparty", "currency", "department", "design", "staff", "sales_order", 
                "address", "payment", "purchase_order", "payment_type", "transaction"],
                "from_time" : "2022-01-01 11:30:55.00",
                "to_time" : "2025-06-02 11:31:55.00", "raw_data_bucket" : "tt-raw-data"
                }'''
    lambda_handler(event, {})