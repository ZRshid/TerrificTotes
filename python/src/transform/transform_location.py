import pandas as pd

def transform_location(address: pd.DataFrame) -> pd.DataFrame:
    """transform the address dataframe to dim_address table

    Args:
        address (pd.DataFrame): the address dataframe

    Returns:
        pd.DataFrame: dim_address from star schema
    """

    df_dropped_columns = address.drop(["created_at", "last_updated", "from_time" ,"to_time"], axis='columns', errors="ignore")
    df_changed_name = df_dropped_columns.rename(columns={"address_id": "location_id"})
    return df_changed_name