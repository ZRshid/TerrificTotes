import pandas as pd
from sqlalchemy import create_engine
import logging


def create_sql(
    df: pd.DataFrame,
    table_name: str,
    user: str,
    password: str,
    host: str,
    database: str,
) -> int:
    """Inserts dataframe into database

    Args:
        df (pd.DataFrame): dataframe to be inserted
        table_name (str): the table name of dataframe
        user (str): username of database
        password (str): password of database
        host (str): host of database
        database (str): database of database

    Returns:
        int: returns number of rows inserted
    """
    try:
        DATABASE_URL = f"postgresql+pg8000://{user}:{password}@{host}/{database}"

        # Create connection to PostgreSQL
        engine = create_engine(DATABASE_URL)

        df.to_sql(table_name, engine, schema="public", index=False, method="multi")
        logging.info(msg="successfully inserted into database")
        return len(df)
    except Exception as e:
        logging.error(msg=f"error inserting into database {e}")
        raise e
