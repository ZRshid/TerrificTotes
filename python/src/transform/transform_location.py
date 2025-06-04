import pandas as pd
import json

def transform_location(address: pd.DataFrame) -> pd.DataFrame:
    #create new dataframe using address changing it to location
    #create address_id column
    #drop created and last updated columns
    #return dataframe
    # print(address)
    df = address.loc["address"]
    print(df)
    return address