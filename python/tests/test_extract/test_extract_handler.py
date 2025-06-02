from python.src.extract.extract_handler import lambda_handler 
import pytest 
import json
import os  

## extract one table and save it to the raw data bucket 

# mock/patch logging - returns a log - message info 

# test if the log returns what we expect 


# test if lambda returns list of tables uploaded  
@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

@pytest.fixture()
def event():
    return '''{"tables" : ["table_name"],
                "from_time" : "2025-06-02 11:30:55.00",
                 "to_time" : "2025-06-02 11:31:55.00", "raw_data_bucket" : "tt-raw-data"
                 }'''

# @pytest.fixture()
# def context():

class TestLambdaHandler():

    def test_lambda_handler_returns_dict(self, event):

        result = lambda_handler(event, {}) 

        assert isinstance(result, dict)
        #assert isinstance(result[]) 

    def test_lambda_handler_returned_dict_keys_matching(self,event):

        expected_keys = "tables"

        result = lambda_handler(event, {}) 

        assert expected_keys in result 

    def test_lambda_handler_returns_dict_lists(self, event):

        result = lambda_handler(event, {}) 

        assert isinstance(result["tables"], list)
        

# test extract and returns one table
    def test_lambda_handler_extracts_and_return_one_table(self, event):
        expected_result = ["table_name"]

        result = lambda_handler(event, {}) 

        assert result == expected_result

    
# test if the data have been saved