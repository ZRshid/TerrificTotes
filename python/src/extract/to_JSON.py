import json

def to_JSON(table_name:str, columns_data:list,rows:list[list],)->str:
    """Converts the response from the database request into some json with the form:\n
    {"table_name":[{"col0":value,col...:value,coln-1:value},{{"col0":value,...,coln-1:value},...}]}

    Args:
        table_name (str): The name of a table
        columns_data (list): pg8000 columns dictionary
        rows (list[list]): A list of rows

    Returns:
        str: A json string (see above)
    """ 
    column_names = extract_names_from_columns_data(columns_data)
    named_rows = name_rows(rows, column_names)
    table_dict = {table_name:named_rows}

    return json.dumps(table_dict, default=str)

def name_rows(rows:list, column_names:list) -> list:

    named_rows = []
    for row in rows:
        if len(row) != len(column_names):
            raise LengthMissMatchException(f"length of row does not match number of columns:{row},{column_names}")
        named_row = {col:value for col, value in zip(column_names,row)}
        named_rows.append(named_row)
    return named_rows

def extract_names_from_columns_data(columns_data:list) -> list:
    return [col['name'] for col in columns_data] #Are there any circumstances where name is not in the dictionary? PG8000's doc are terrible
    
    
class LengthMissMatchException(Exception):
    pass