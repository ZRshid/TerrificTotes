import pandas as pd


def transform_counterparty(
    counterparty: pd.DataFrame, address: pd.DataFrame
) -> pd.DataFrame:
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
    
    return df_renamed_merged