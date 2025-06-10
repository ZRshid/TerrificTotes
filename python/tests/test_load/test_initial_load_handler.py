import pytest
import os
from src.load.initial_load_handler import lambda_handler,insert_parquet_file_to_db
from unittest.mock import patch

@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

@patch("src.load.initial_load_handler.get_secret")
@patch("src.load.initial_load_handler.insert_parquet_file_to_db")
class TestLambda_hander:
   
    def test_returns_dict(self,insert,get_secret):
        get_secret.return_value = {'username':'test', 
                                   'password':'test',
                                   'engine':'test',
                                   'host':'test',
                                   'port':'test',
                                   'dbname':'test'
                                   }
        insert.return_value = 1
        
        event = {'timestamp':"2025-06-02 23:59:59.00","tables":[]}
        context = {}
        
        result = lambda_handler(event,context)

        assert isinstance(result,dict)
    def test_returns_with_keys(self,insert,get_secret):
        get_secret.return_value = {'username':'test', 
                            'password':'test',
                            'engine':'test',
                            'host':'test',
                            'port':'test',
                            'dbname':'test'
                            }
        insert.return_value = 1
        event = {'timestamp':"2025-06-02 23:59:59.00","tables":[]}
        context = {}
        expected_keys = ['tables','timestamp']
        
        result = lambda_handler(event,context)

        for key in expected_keys:
            assert key in result

    def test_returns_dictionary_tables_data_has_correct_keys(self,insert,get_secret):
        get_secret.return_value = {'username':'test', 
                            'password':'test',
                            'engine':'test',
                            'host':'test',
                            'port':'test',
                            'dbname':'test'
                            }
        insert.return_value = 1
        tables = ["currency"]
        event = {
            'timestamp':"2025-06-02 23:59:59.00",
            "tables":tables}
        context = {}
        expected_keys = ['name','inserted_rows']
        result = lambda_handler(event,context)
        for key in expected_keys:
            assert key in result['tables'][0]

    def test_returns_dictionary_tables_data_has_correct_len(self,insert,get_secret):
        get_secret.return_value = {'username':'test', 
                                   'password':'test',
                                   'engine':'test',
                                   'host':'test',
                                   'port':'test',
                                   'dbname':'test'
                                   }
        insert.return_value = 1
        tables = ["dim_currency","dim_staff"]
        event = {
            'timestamp':"2025-06-02 23:59:59.00",
            "tables":tables}
        context = {}
        expected_number = 2

        result = lambda_handler(event,context)
        assert  len(result['tables'])==expected_number
    
    def test_raises(self,insert,get_secret):
        get_secret.return_value = {'username':'test', 
                            'password':'test',
                            'engine':'test',
                            'host':'test',
                            'port':'test',
                            'dbname':'test'
                            }
        get_secret.side_effect= ValueError()
        
        event = {'timestamp':"2025-06-02 23:59:59.00","tables":[]}
        context = {}
        ##after puting in logs make sure still raises
        with pytest.raises(Exception) as e:
            lambda_handler(event,context)

class TestInsert_parquet_file_to_db:
    ...
class TestMake_parquet_key:
    pass
