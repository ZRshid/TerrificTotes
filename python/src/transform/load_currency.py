import pandas as pd 



def load_currency_codes(file:str, columns:list[str]) -> pd.DataFrame:
     
    currency_df = pd.read_csv(file, usecols=columns)
    
    currency_df['currency_id'] = currency_df.index     
    print(currency_df)
    return currency_df
