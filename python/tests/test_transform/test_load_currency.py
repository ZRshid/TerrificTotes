from src.transform.transform_currency import load_currency_codes
import pandas as pd  
import pytest 

class Test_Load_Currency_Codes():
    
    def test_func_return_df(self):
        df = pd.DataFrame 
        file = "../Data/Currency-codes.csv"
        headers = ["currency_code", "currency_name"]
        result = load_currency_codes(file, headers)
        assert isinstance(result, pd.DataFrame)

    def test_func_returns_df_with_right_columns_names(self):
        df = pd.DataFrame 
        file = "../Data/Currency-codes.csv"
        headers_csv = ["currency_code", "currency_name"]
        result_df = load_currency_codes(file, headers_csv) # df
        columns = result_df.columns.to_list()
        
        assert "currency_code" in columns
        assert "currency_name" in columns 

    def test_func_returns_df(self):
        df = pd.DataFrame 
        file = "../Data/Currency-codes.csv"
        headers_csv = ["currency_code", "currency_name"]
        result_df = load_currency_codes(file, headers_csv)
        columns = result_df.columns.to_list()

        assert "currency_id" in columns 



