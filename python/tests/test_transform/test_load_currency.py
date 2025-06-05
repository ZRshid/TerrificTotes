from python.src.transform.load_currency import load_currency_codes, load_currency_codes_from_s3
import pandas as pd  
import pytest 
from unittest.mock import patch
import awswrangler as wr

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
        result_df = load_currency_codes(file, headers_csv)
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


    @patch("awswrangler.s3.read_csv")
    def test_func_loads_codes_from_s3(self, mock_read_csv):
      
        mock_read_csv.return_value = pd.DataFrame({
            "currency_code": ["USD", "EUR"],
            "currency_name": ["US Dollar", "Euro"]
        })

   
        result = load_currency_codes_from_s3(columns=["currency_code", "currency_name"])
      
        assert isinstance(result, pd.DataFrame)
       
        assert "currency_id" in result.columns
        
        assert result.shape[0] == 2 
     






            
