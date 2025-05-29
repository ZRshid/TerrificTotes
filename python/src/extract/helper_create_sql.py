from pg8000.native import  identifier, literal
import datetime

#time utc

def create_sql(table:str,columns:list,from_time:datetime,to_time:datetime) -> str:
    """_summary_

    Args:
        table (str): _description_
        columns (list): _description_
        from_time (datetime): _description_
        to_time (datetime): _description_

    Returns:
        str: _description_
    """    
    return "nothing"
