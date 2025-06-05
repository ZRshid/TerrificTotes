import pandas as pd 
import awswrangler as wr

def load_currency_codes_from_s3(columns:list[str], path=['s3://zip-bucket/currency-codes.csv']):
    def load_currency_codes_from_s3(columns: list[str], path: list[str] = ['s3://zip-bucket/currency-codes.csv']) -> pd.DataFrame:
        """
        Loads currency codes from an S3 bucket into a pandas DataFrame.

        Args:
            columns (list[str]): A list of column names to select from the CSV file.
            path (list[str], optional): A list containing the S3 path to the CSV file. Defaults to ['s3://zip-bucket/currency-codes.csv'].

        Returns:
            pd.DataFrame: A pandas DataFrame containing the selected columns from the CSV file, 
                          with an additional 'currency_id' column generated from the DataFrame index.
        """
    currency_df = wr.s3.read_csv(path, usecols=columns)
    currency_df['currency_id'] = currency_df.index  
    return currency_df

def load_currency_codes(file:str, columns:list[str]) -> pd.DataFrame:
    def load_currency_codes(file: str, columns: list[str]) -> pd.DataFrame:
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
    
    currency_df['currency_id'] = currency_df.index     
    print(currency_df)
    return currency_df


    