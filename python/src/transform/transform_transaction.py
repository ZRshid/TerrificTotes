import pandas as pd
import logging

def transform_transaction(transaction: pd.DataFrame) -> pd.DataFrame:
    """transforms the transaction dataframe into dim_transaction
    which drops non_essential metadata columns

    Args:
        transaction (pd.DataFrame): the original dataframe

    Returns:
        pd.DataFrame: a dim_transaction dataframe, return columns named transaction_id, transaction_type, sales_order_id, purchase_order_id
    """
    try:
        df_dim_transaction = transaction.drop(["created_at", "last_updated"],
                                        axis="columns",
                                        errors="ignore")
        return df_dim_transaction
    except Exception as e:
        logging.error(msg=f"fail to create dim_transaction due to error: {e}")
        raise e
