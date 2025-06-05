import pandas as pd
import logging

def dim_date(df_sales_order: pd.DataFrame) -> pd.DataFrame:
    """
    Create a date dimension table from the sales order data.
    Args:
        df_sales_order (pd.DataFrame): DataFrame containing sales order data with date columns.
    Returns:
        pd.DataFrame: DataFrame containing the date dimension with date_id, year, month, day, 
                      day_of_week, day_name, month_name, and quarter.
    """
    try:
        df_sales_order_date = df_sales_order[["created_at", "last_updated", 
                            "agreed_payment_date", "agreed_delivery_date"]]
    
        # Convert timestamp into date format
        df_sales_order_date["created_at"] = pd.to_datetime(df_sales_order_date["created_at"], utc=True).dt.normalize()
        df_sales_order_date["last_updated"] = pd.to_datetime(df_sales_order_date["last_updated"], utc=True).dt.normalize()
        # Convert string into date format
        df_sales_order_date["agreed_payment_date"] = pd.to_datetime(df_sales_order_date["agreed_payment_date"], utc=True).dt.normalize()
        df_sales_order_date["agreed_delivery_date"] = pd.to_datetime(df_sales_order_date["agreed_delivery_date"], utc=True).dt.normalize()

        # Concatenate all date columns into a single Series, drop duplicates
        date = pd.concat([df_sales_order_date["created_at"], df_sales_order_date["last_updated"], 
                            df_sales_order_date["agreed_payment_date"], df_sales_order_date["agreed_delivery_date"]],
                            ignore_index=True)
        date.drop_duplicates(inplace=True, ignore_index=True)

        d = {"date_id": date.dt.date, "year": date.dt.year, "month": date.dt.month, "day": date.dt.day, 
            "day_of_week": date.dt.dayofweek, "day_name": date.dt.day_name(), "month_name": date.dt.month_name(), "quarter": date.dt.quarter}
        
        df_dim_date = pd.DataFrame(d)
        logging.info("Date dimension table is successfully updated!")
        return df_dim_date
    
    except Exception as e:
        logging.error("Date dimension table cannot be generated")
        raise e