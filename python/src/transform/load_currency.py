import pandas as pd 
import awswrangler as wr
import logging

def load_currency_codes_from_s3(columns:list[str], path=['s3://tt-zip-bucket/currency-codes.csv']):
    """
    Loads currency codes from an S3 bucket into a pandas DataFrame.

    Args:
        columns (list[str]): A list of column names to select from the CSV file.
        path (list[str], optional): A list containing the S3 path to the CSV file. Defaults to ['s3://tt-zip-bucket/currency-codes.csv'].

    Returns:
        pd.DataFrame: A pandas DataFrame containing the selected columns from the CSV file, 
                        with an additional 'currency_id' column generated from the DataFrame index.
    """
    try:
        currency_df = wr.s3.read_csv(path, usecols=columns)
        currency_df = sanitize_rows(currency_df)
        currency_df['currency_id'] = currency_df.index  
        return currency_df
    except Exception as e:
        logging.error(f"can not load currency from {path} or {e}")

def load_currency_codes(file:str, columns:list[str]) -> pd.DataFrame:
    """
    Load currency codes from a CSV file and return a DataFrame.
    Args:
        file (str): The file path to the CSV file containing currency data.
        columns (list[str]): A list of column names to be loaded from the CSV file.
    Returns:
        pd.DataFrame: A DataFrame containing the specified columns from the CSV file,
                        with an additional 'currency_id' column generated from the index.
    """
     
    currency_df = pd.read_csv(file, usecols=columns)
    currency_df = sanitize_rows(currency_df)
    currency_df['currency_id'] = currency_df.index     
    return currency_df

def sanitize_rows(currency_df:pd.DataFrame,column_subset = ["currency_code", "currency_name"]) -> pd.DataFrame:
    """Return a dataframe without null values or duplicate rows

    Args:
        currency_df (pd.DataFrame): a dataframe

    Returns:
        pd.DataFrame: A new dataframe without nulls or duplicate rows
    """    
    currency_df =currency_df.dropna()
    currency_df = currency_df.drop_duplicates(subset=column_subset)
    currency_df = currency_df.reset_index(drop=True)
    return currency_df

if __name__ == "__main__":
    load_currency_codes_from_s3(["currency_code", "currency_name"], path=['s3://tt-zip-bucket/currency-codes.csv'])
    