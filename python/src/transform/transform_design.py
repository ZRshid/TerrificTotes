import pandas as pd
import logging

def transform_design(design:pd.DataFrame):
    
    """
    Saves the transformed DataFrame in its correct format to match the project star schema
    Args:
        design (pd.DataFame): The name of the table being transformed    
    Returns:
        The transformed table 
    Raises:
        Exception: If there is an error when tarnaforming the design table .
    """
    try:
        df_updated_design_table = design.drop(columns=["created_at", "last_updated"] , axis =1)
        df_ascending_order = df_updated_design_table.sort_values(by="design_id", ascending=True)
        df_set_index = df_ascending_order.set_index("design_id")
        return df_set_index
    except Exception as e:
        logging.error(msg=f"Failed to make the design datafram: {e}")
        raise e



