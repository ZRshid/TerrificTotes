import pandas as pd
import logging

def transform_payment_type(payment_type: pd.DataFrame) -> pd.DataFrame:
    """transforms the payment_types dataframe into dim_payment_types
    which drops non_essential metadata columns
    Args:
        payment_type (pd.DataFrame): the original dataframe

    Raises:
        e: catches any error not caught

    Returns:
        pd.DataFrame: a dim_payment_types dataframe
    """
    try:
        df_dropped = payment_type.drop(["created_at", "last_updated"],
                                        axis="columns",
                                        errors="ignore")
        return df_dropped
    except Exception as e:
        logging.error(msg=f"fail to create dim_payment_type due to error: {e}")
        raise e