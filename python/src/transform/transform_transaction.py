import pandas as pd
import logging

def transform_transaction(transaction: pd.DataFrame) -> pd.DataFrame:
    """transforms the transaction dataframe into dim_transaction
    which drops non_essential metadata columns

    Args:
        transaction (pd.DataFrame): the original dataframe

    Raises:
        e: catches any error not caught

    Returns:
        pd.DataFrame: a dim_transaction dataframe
    """
    try:
        df_dropped = transaction.drop(["created_at", "last_updated"],
                                        axis="columns",
                                        errors="ignore")
        return df_dropped
    except Exception as e:
        logging.error(msg=f"fail to create dim_transaction due to error: {e}")
        raise e