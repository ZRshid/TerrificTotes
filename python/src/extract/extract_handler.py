import logging
from datetime import datetime


logger = logging.getLogger() #This line creates a tool to write messages about what our program is doing
logger.setLevel(logging.INFO) #This line tells that tool to only pay attention to important messages and above

def lambda_handler(event, context):
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    try:
        if "tables" in event and len(event["tables"]) > 0: 
            logger.info(f"extract succeeded: {len(event['tables'])} tables found at {formatted_time}")
            return {
                "status": "success",
                "message": f"Extracted {len(event['tables'])} tables.",
                "tables": event["tables"]
            }
        else:
            raise ValueError("Missing or empty tables list") #Signals an error when something is missing such as tables etc.     
    except Exception as err:
        logger.error(f"Extraction has failed {err}")
        return {
              "status": "error",
                "message": f"Extract failed: {err}"
            }
    
if __name__ == "__main__":
    test_event = {"tables": ["table_name","sales"],
                  "from_time" : "2025-06-02 11:30:55.00",
                  "to_time" : "2025-06-02 11:31:55.00",
                  "raw_data_bucket" : "tt-raw-data"}           
    result = lambda_handler(test_event, None)
    print(result)





