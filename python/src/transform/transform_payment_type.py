import pandas as pd
import logging

def transform_payment_type(payment_type: pd.DataFrame) -> pd.DataFrame:
    """transforms the payment_types dataframe into dim_payment_types
    which drops non_essential metadata columns
    Args:
        payment_type (pd.DataFrame): the original dataframe
    
    Returns:
        pd.DataFrame: a dim_payment_types dataframe, returns consists of two columns: payment_type_id and payment_type_name 
    """
    try:
        df_dim_payment_type = payment_type.drop(["created_at", "last_updated"],
                                        axis="columns",
                                        errors="ignore")
        return df_dim_payment_type
    except Exception as e:
        logging.error(msg=f"fail to create dim_payment_type due to error: {e}")
        raise e
