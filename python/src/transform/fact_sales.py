import pandas as pd

def sales_facts(df_sales_order: pd.DataFrame, df_dim_counterparty: pd.DataFrame, 
                df_dim_currency: pd.DataFrame,  df_dim_design: pd.DataFrame,
                df_dim_date: pd.DataFrame, df_dim_location: pd.DataFrame,
                df_dim_staff: pd.DataFrame):

    expected_columns = ["sales_order_id", "created_date", "created_time", 
                                    "last_updated_date", "last_updated_time", "sales_staff_id", "counterparty_id",
                                    "units_sold", "unit_price", "currency_id", "design_id", "agreed_payment_date",
                                    "agreed_delivery_date", "agreed_delivery_location_id"]

    df_sales_facts = pd.DataFrame(columns=expected_columns)

    
    # Convert timestamp into date format
    df_sales_facts["created_date"] = pd.to_datetime(df_sales_order["created_at"], utc=True).dt.date
    df_sales_facts["last_updated_date"] = pd.to_datetime(df_sales_order["last_updated"], utc=True).dt.date
    df_sales_facts["last_updated_time"] = pd.to_datetime(df_sales_order["last_updated"], utc=True).dt.time 
    df_sales_facts["created_time"] = pd.to_datetime(df_sales_order["created_at"], utc=True).dt.time 
     
    df_sales_facts["units_sold"] = df_sales_order["units_sold"]
    df_sales_facts["unit_price"] = df_sales_order["unit_price"]

        # Convert string into date format
    df_sales_facts["agreed_payment_date"] = pd.to_datetime(df_sales_order["agreed_payment_date"], utc=True).dt.date
    df_sales_facts["agreed_delivery_date"] = pd.to_datetime(df_sales_order["agreed_delivery_date"], utc=True).dt.date

    df_sales_facts["sales_order_id"] = df_sales_order["sales_order_id"]
    df_sales_facts["sales_staff_id"] = df_sales_order["staff_id"]
    df_sales_facts["counterparty_id"] = df_sales_order["counterparty_id"]
    df_sales_facts["currency_id"] = df_sales_order["currency_id"]
    df_sales_facts["design_id"] = df_sales_order["design_id"]
    df_sales_facts["agreed_delivery_location_id"] = df_sales_order["agreed_delivery_location_id"]

    df_sales_facts.reset_index(inplace=True)
    df_sales_facts.rename(columns={"index": "sales_record_id"}, inplace=True)
    
    df_sales_facts.to_csv("src/transform.csv")
    return df_sales_facts 

