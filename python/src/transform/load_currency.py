import pandas as pd 
import awswrangler as wr

def load_currency_codes_from_s3(columns:list[str], path=['s3://zip-bucket/currency-codes.csv']):
    currency_df = wr.s3.read_csv(path, usecols=columns)
    currency_df['currency_id'] = currency_df.index  
    return currency_df

def load_currency_codes(file:str, columns:list[str]) -> pd.DataFrame:
     
    currency_df = pd.read_csv(file, usecols=columns)
    
    currency_df['currency_id'] = currency_df.index     
    print(currency_df)
    return currency_df


    