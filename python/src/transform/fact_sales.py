import pandas as pd

def sales_facts(df_sales_order: pd.DataFrame, df_dim_counterparty: pd.DataFrame, 
                df_dim_currency: pd.DataFrame,  df_dim_design: pd.DataFrame,
                df_dim_date: pd.DataFrame, df_dim_location: pd.DataFrame,
                df_dim_payment_type: pd.DataFrame, df_dim_staff: pd.DataFrame):
                
    
    # create an empty df 

    # operate on each column of the df_sales_order table as series 

        # convert the series in the new format which can be more than one column or it could be an id of a dimension 
        
            # link data to dim tables 
            # renaming columns 

        # add each converted series to the empty df 

    df_sales_facts = pd.DataFrame()
    df_sales_order
    pass