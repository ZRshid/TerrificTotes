import pandas as pd
from sqlalchemy import create_engine

def create_sql(
    df: pd.DataFrame,
    table_name: str,
    user: str,
    password: str,
    host: str,
    database: str,
):
    DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

    # Create connection to PostgreSQL
    engine = create_engine(DATABASE_URL)

    df.to_sql(table_name, engine, schema="public", index=False, method="multi")
