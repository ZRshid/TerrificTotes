import pandas as pd
import logging
import gc

def sales_facts(df_sales_order: pd.DataFrame):
    """
    Transforms the sales order data into a sales facts DataFrame.
    Args:
        df_sales_order (pd.DataFrame): DataFrame containing sales order data with columns:
            - sales_order_id
            - created_at
            - last_updated
            - design_id
            - staff_id
            - counterparty_id
            - units_sold
            - unit_price
            - currency_id
            - agreed_delivery_date
            - agreed_payment_date
            - agreed_delivery_location_id
    Returns:
        pd.DataFrame: Transformed DataFrame with sales facts, including:
            - sales_record_id
            - sales_order_id
            - created_date
            - created_time
            - last_updated_date
            - last_updated_time
            - sales_staff_id
            - counterparty_id
            - units_sold
            - unit_price
            - currency_id
            - design_id
            - agreed_payment_date
            - agreed_delivery_date
            - agreed_delivery_location_id 
    """
    try:
        expected_columns = ["sales_order_id", "created_date", "created_time", 
                                        "last_updated_date", "last_updated_time", "sales_staff_id", "counterparty_id",
                                        "units_sold", "unit_price", "currency_id", "design_id", "agreed_payment_date",
                                        "agreed_delivery_date", "agreed_delivery_location_id"]

        df_sales_facts = pd.DataFrame(columns=expected_columns)
        
        new = df_sales_order.copy

        # Convert timestamp into date/time format
        
        df_sales_order["created_date"] = pd.to_datetime(df_sales_order["created_at"], utc=True)
        df_sales_order["created_time"] = pd.to_datetime(df_sales_order["created_at"], utc=True).dt.time 
        df_sales_order.drop(columns="created_at")
        df_sales_order["last_updated_date"] = pd.to_datetime(df_sales_order["last_updated"], utc=True).dt.date
        df_sales_order["last_updated_time"] = pd.to_datetime(df_sales_order["last_updated"], utc=True).dt.time 
        df_sales_order.drop(columns="last_updated")
        logging.info("sales_facts - created and updated times done")
        # Convert string into date format
        df_sales_order["agreed_payment_date"] = pd.to_datetime(df_sales_order["agreed_payment_date"], utc=True).dt.date
        df_sales_order["agreed_delivery_date"] = pd.to_datetime(df_sales_order["agreed_delivery_date"], utc=True).dt.date
        df_sales_order.drop(columns="agreed_delivery_date")
        logging.info("sales_facts - delivery_date done")
        

        # df_sales_facts["units_sold"] = df_sales_order["units_sold"]
        # df_sales_order.drop(columns="units_sold")
        # df_sales_facts["unit_price"] = df_sales_order["unit_price"]
        # df_sales_order.drop(columns="unit_price")
        # df_sales_facts["sales_order_id"] = df_sales_order["sales_order_id"]
        # df_sales_order.drop(columns="sales_order_id")
        # df_sales_facts["sales_staff_id"] = df_sales_order["staff_id"]
        # df_sales_order.drop(columns="staff_id")
        # df_sales_facts["counterparty_id"] = df_sales_order["counterparty_id"]
        # df_sales_order.drop(columns="counterparty_id")
        # df_sales_facts["currency_id"] = df_sales_order["currency_id"]
        # df_sales_order.drop(columns="currency_id")
        # df_sales_facts["design_id"] = df_sales_order["design_id"]
        # df_sales_order.drop(columns="design_id")
        # df_sales_facts["agreed_delivery_location_id"] = df_sales_order["agreed_delivery_location_id"]
        # df_sales_order.drop(columns="agreed_delivery_location_id")
        # Reset index and rename the index column to sales_record_id
        df_sales_facts.reset_index(inplace=True)
        df_sales_facts.rename(columns={"index": "sales_record_id"}, inplace=True)
        
        logging.info(msg="fact_sales_order table has been generated")
        return df_sales_order ##now returning same table
    except Exception as e:
        logging.error(msg=f"fact_sales_order table has not been generated: {e}")
        raise e
