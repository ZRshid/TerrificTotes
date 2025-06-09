from src.transform.load_currency import load_currency_codes, load_currency_codes_from_s3, sanitize_rows
import pandas as pd
import pytest 
from unittest.mock import patch
import awswrangler as wr
import os
from io import StringIO

CURRENCY_CSV ="""
country,currency_name,currency_code
AFGHANISTAN,Afghani,AFN
ÅLAND ISLANDS,Euro,EUR
ALBANIA,Lek,ALL
ALGERIA,Algerian Dinar,DZD
AMERICAN SAMOA,US Dollar,USD
ANDORRA,Euro,EUR
ANGOLA,Kwanza,AOA
ANGUILLA,East Caribbean Dollar,XCD
ANTARCTICA,No universal currency,
ANTIGUA AND BARBUDA,East Caribbean Dollar,XCD
ARAB MONETARY FUND,Arab Accounting Dinar,XAD
ARGENTINA,Argentine Peso,ARS
ARMENIA,Armenian Dram,AMD
ARUBA,Aruban Florin,AWG
AUSTRALIA,Australian Dollar,AUD
AUSTRIA,Euro,EUR
"""
AFTER_CSV ="""
country,currency_name,currency_code
AFGHANISTAN,Afghani,AFN
ÅLAND ISLANDS,Euro,EUR
ALBANIA,Lek,ALL
ALGERIA,Algerian Dinar,DZD
AMERICAN SAMOA,US Dollar,USD
ANGOLA,Kwanza,AOA
ANGUILLA,East Caribbean Dollar,XCD
ARAB MONETARY FUND,Arab Accounting Dinar,XAD
ARGENTINA,Argentine Peso,ARS
ARMENIA,Armenian Dram,AMD
ARUBA,Aruban Florin,AWG
AUSTRALIA,Australian Dollar,AUD
"""
@pytest.fixture
def filepath():
    cwd = os.getcwd()
    if cwd.endswith("python"):
        cwd = cwd[:-7]
    return cwd+"/Data/Currency-codes.csv"

@pytest.fixture
def currency_df():
    currency_df= pd.read_csv(StringIO(CURRENCY_CSV), usecols=["currency_code", "currency_name"])
    return currency_df
@pytest.fixture
def expected_df():
    currency_df= pd.read_csv(StringIO(AFTER_CSV), usecols=["currency_code", "currency_name"])
    return currency_df

class Test_Load_currency_codes():
    
    def test_func_return_df(self,filepath):
        df = pd.DataFrame
        print(os.getcwd())

        headers = ["currency_code", "currency_name"]
        result = load_currency_codes(filepath, headers)
        assert isinstance(result, pd.DataFrame)

    def test_func_returns_df_with_right_columns_names(self,filepath):
        df = pd.DataFrame 
        
        headers_csv = ["currency_code", "currency_name"]
        result_df = load_currency_codes(filepath, headers_csv)
        columns = result_df.columns.to_list()
        
        assert "currency_code" in columns
        assert "currency_name" in columns
        assert "currency_id" in columns
    def test_currency_id_is_sequential(self,filepath ):
        result = load_currency_codes(filepath,columns=["currency_code", "currency_name"])
        assert (result["currency_id"].diff()[1:]==1).all()
        
class TestLoad_currency_codes_from_s3():
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
    @patch("awswrangler.s3.read_csv")
    def test_currency_id_is_sequential(self, mock_read_csv,currency_df ):
        mock_read_csv.return_value = currency_df
        result = load_currency_codes_from_s3(columns=["currency_code", "currency_name"])
        assert (result["currency_id"].diff()[1:]==1).all()


    class TestSanitize_rows():
        def test_returns_df(self,currency_df):
            result = sanitize_rows(currency_df)
            assert isinstance(result, pd.DataFrame)
            assert result is not currency_df
        def test_has_no_nulls(self,currency_df):
            result = sanitize_rows(currency_df)
            assert result[["currency_code", "currency_name"]].notnull().values.all()
        def test_returns_correct_df(self,currency_df,expected_df):
            result = sanitize_rows(currency_df)
            pd.testing.assert_frame_equal(result,expected_df)
            
     






            
