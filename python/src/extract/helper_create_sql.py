from pg8000.native import identifier, literal
import datetime

# time utc


def create_sql(table: str, from_time: datetime, to_time: datetime) -> str:
    """produces a sql string that selects all columns from a given table with a
    time from and to from a given time

    Args:
        table (str): table extracting from
        from_time (datetime): data from this time
        to_time (datetime): data to this time

    Returns:
        str: the sql query
    """
    where_clause = add_where_clause(from_time, to_time)
    return f"SELECT * FROM {identifier(table)} {where_clause};"


def add_where_clause(from_time: datetime, to_time: datetime) -> str:
    """creates the where clause"""
    str_from_time = from_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    str_to_time = to_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(literal(from_time), str_to_time)
    return f"WHERE last_updated BETWEEN {literal(str_from_time)} and {literal(str_to_time)}"
