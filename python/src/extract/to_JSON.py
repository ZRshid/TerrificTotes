import json
from datetime import datetime
from python.utils.utils import datetime_to_str

def to_JSON(table_name:str, columns_data:list,rows:list[list], from_time: datetime|None = None, to_time: datetime|None = None)->str:
    """Converts the response from the database request into some json with the form:\n
    {"table_name":[{"col0":value,col...:value,coln-1:value},{{"col0":value,...,coln-1:value},...}]}
    
    If to_time of from_time are not none then they will be keys in the json with
    their dt converted as their value.
    Args:
        table_name (str): The name of a table
        columns_data (list): pg8000 columns dictionary
        rows (list[list]): A list of rows
        from_time (datetime | None, optional): early limit of the extraction. Defaults to None.
        to_time (datetime | None, optional): last extraction time. Defaults to None.

    Returns:
        str: A json string (see above)
    """ 
    column_names = extract_names_from_columns_data(columns_data)
    named_rows = name_rows(rows, column_names)
    table_dict = {table_name:named_rows}

    add_time_keys(from_time, to_time, table_dict)

    return json.dumps(table_dict, default=str)

def add_time_keys(from_time, to_time, table_dict):
    """adds times to the first level of dictionary"""
    if from_time != None:
        table_dict['from_time'] = datetime_to_str(from_time)
    if to_time != None:
        table_dict['to_time'] = datetime_to_str(to_time)

def name_rows(rows:list, column_names:list) -> list:
    """Gives each value in each row a name"""

    named_rows = []
    for row in rows:
        if len(row) != len(column_names):
            raise LengthMissMatchException(f"length of row does not match number of columns:{row},{column_names}")
        named_row = {col:value for col, value in zip(column_names,row)}
        named_rows.append(named_row)
    return named_rows

def extract_names_from_columns_data(columns_data:list) -> list:
    """just extracts the name values into a list
     (N.b no error checking etc)
     """
    return [col['name'] for col in columns_data] #Are there any circumstances where name is not in the dictionary? PG8000's doc are terrible
    
    
class LengthMissMatchException(Exception):
    pass