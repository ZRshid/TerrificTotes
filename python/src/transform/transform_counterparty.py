import pandas as pd
import logging


def transform_counterparty(
    counterparty: pd.DataFrame, address: pd.DataFrame
) -> pd.DataFrame:
    """create dim_counterparty by merging counterparty 
    and address dataframe with address_id and then dropping/renaming columns

    Args:
        counterparty (pd.DataFrame): original counterparty dataframe
        address (pd.DataFrame): the address dataframe

    Returns:
        pd.DataFrame: a dataframe with columns: {
                "counterparty_id",
                "counterparty_legal_name",
                "counterparty_legal_address_line_1",
                "counterparty_legal_address_line_2",
                "counterparty_legal_district",
                "counterparty_legal_city",
                "counterparty_legal_postal_code",
                "counterparty_legal_country",
                "counterparty_legal_phone_number",
            }
    """
    
    if not isinstance(counterparty, pd.DataFrame):
        raise TypeError("counterparty is a dataframe")
    if not isinstance(address, pd.DataFrame):
        raise TypeError("address is a dataframe")
    
    required_counterparty_columns = {"counterparty_id", "counterparty_legal_name", "legal_address_id"}
    required_address_columns = {"address_id", "address_line_1", "city", "postal_code", "country", "phone"}

    if not required_counterparty_columns.issubset(counterparty.columns):
        missing = required_counterparty_columns - set(counterparty.columns)
        raise ValueError(f"required columns missing in counterparty: {missing}")
    
    if not required_address_columns.issubset(address.columns):
        missing = required_address_columns - set(address.columns)
        raise ValueError(f"required columns missing in address: {missing}")
    
    try:
        df_drop_address = address.drop(
            ["created_at", "last_updated", "from_time", "to_time"],
            axis="columns",
            errors="ignore",
        )

        df_merged = pd.merge(
            counterparty,
            df_drop_address,
            how="left",
            left_on="legal_address_id",
            right_on="address_id",
        )

        df_merged_drop = df_merged.drop(
            [
                "created_at",
                "last_updated",
                "commercial_contact",
                "delivery_contact",
                "address_id",
                "legal_address_id",
            ],
            axis="columns",
            errors="ignore",
        )

        df_renamed_merged = df_merged_drop.rename(
            columns={
                "address_line_1": "counterparty_legal_address_line_1",
                "address_line_2": "counterparty_legal_address_line_2",
                "district": "counterparty_legal_district",
                "city": "counterparty_legal_city",
                "postal_code": "counterparty_legal_postal_code",
                "country": "counterparty_legal_country",
                "phone": "counterparty_legal_phone_number",
            }
        )
        logging.info(msg="successfully create dim_counterparty")
        return df_renamed_merged
    except Exception as e:
        logging.error(msg=f"failed to create dim_counterparty dataframe due to error: {e}")
        raise e(f"failed to create dim_counterparty dataframe due to error: {e}")