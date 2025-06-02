from pg8000.native import Connection, InterfaceError, DatabaseError
from dotenv import load_dotenv
import os
from datetime import datetime
import decimal
import logging

load_dotenv()


# this will change to the secrets that contains the info of database
# instead of using .env
def connect_to_db():
    """creates the connect to the totes db uses info from the .env"""
    return Connection(
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        database=os.getenv("PG_DATABASE"),
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT")),
    )


def close_db(conn):
    conn.close()


def format_result(result):
    """Format the result list by converting datetime and Decimal objects."""
    formatted_result = []
    for row in result:
        formatted_row = []
        for value in row:
            if isinstance(value, datetime):
                formatted_row.append(value.strftime("%Y-%m-%d %H:%M:%S"))
            elif isinstance(value, decimal.Decimal):
                formatted_row.append(float(value))
            else:
                formatted_row.append(value)
        formatted_result.append(formatted_row)
    return formatted_result


def query_db(query: str, conn: Connection) -> tuple:
    """makes the query to the database

    Args:
        query (str): a string that contains the sql query
        conn (Connection): the connection to the database

    Raises:
        DatabaseError: error caused by the database or sql
        InterfaceError: error interfacing to database or pg8000

    Returns:
        tuple: the results and the coloumns in a dict
    """
    try:
        result = conn.run(query)
        return (result, conn.columns)
    except DatabaseError as d:
        logging.error(f"error with database: {d}")
        raise DatabaseError
    except InterfaceError as i:
        logging.error(f"error interfacing to database: {i}")
        raise InterfaceError
    finally:
        close_db(conn)
