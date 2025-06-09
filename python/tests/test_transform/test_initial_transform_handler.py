from src.transform.transform_counterparty import transform_counterparty
from src.transform.initial_transform_handler import lambda_handler, make_key, transform_table, transform_tables,transform_and_combine
from src.transform.transform_location import transform_location
import pytest
import boto3
from moto import mock_aws
import pandas as pd
import os
from unittest.mock import patch, Mock
from pandas.testing import assert_frame_equal

TEST_BUCKET = 'test-bucket'
TEST_TABLE = "address"
TEST_ADDRESS_JSON = """{
    "from_time": "2022-01-02 23:30:00.00", 
    "to_time": "2025-06-02 23:59:59.00", 
    "address": [
        {"address_id": 1, "address_line_1": "6826 Herzog Via", "address_line_2": null, "district": "Avon", "city": "New Patienceburgh", "postal_code": "28441", "country": "Turkey", "phone": "1803 637401", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"},
        {"address_id": 2, "address_line_1": "179 Alexie Cliffs", "address_line_2": null, "district": null, "city": "Aliso Viejo", "postal_code": "99305-7380", "country": "San Marino", "phone": "9621 880720", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}
    ]
}"""
TEST_KEY = "test/test_address.json"

TEST_TABLE2 = "counterparty"
TEST_JSON_COUNTERPARTY = """{
            "counterparty_id": 1,
            "counterparty_legal_name": "Fahey and Sons",
            "legal_address_id": 15,
            "commercial_contact": "Micheal Toy",
            "delivery_contact": "Mrs. Lucy Runolfsdottir",
            "created_at": "2022-11-03 14:20:51.563000",
            "last_updated": "2022-11-03 14:20:51.563000"
        },
        {
            "counterparty_id": 2,
            "counterparty_legal_name": "Leannon, Predovic and Morar",
            "legal_address_id": 28,
            "commercial_contact": "Melba Sanford",
            "delivery_contact": "Jean Hane III",
            "created_at": "2022-11-03 14:20:51.563000",
            "last_updated": "2022-11-03 14:20:51.563000"
        }]
    """
TEST_KEY2 = "test/test_counterparty.json"

@pytest.fixture()
def s3():
    with mock_aws():
        yield boto3.client('s3', region_name='eu-west-2')

@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

@pytest.fixture()
def s3_with_bucket(s3):
    s3.create_bucket(
        Bucket=TEST_BUCKET,
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    s3.put_object(
            Bucket = TEST_BUCKET,
            Body = TEST_ADDRESS_JSON,
            Key = TEST_KEY
    )
    s3.put_object(
            Bucket = TEST_BUCKET,
            Body = TEST_JSON_COUNTERPARTY,
            Key = TEST_KEY2
    )
    return s3

@pytest.fixture()
def event():
    return {"tables" : ["address", "counterparty"]}                

class TestTransformHandler:
    @patch("src.transform.initial_transform_handler.transform_tables")
    def test_lambda_handler_returns_dict(self,t_tables,event):
        t_tables.return_value = {}
        result = lambda_handler(event,{})
        assert isinstance(result,dict)
        
    @patch("src.transform.initial_transform_handler.transform_tables")
    def test_dict_contains_keys(self,t_tables,event):
        t_tables.return_value = {}
        expected_keys = ["transformed_tables","timestamp"]
        result = lambda_handler(event,{})
        assert expected_keys[0] in result
        assert expected_keys[1] in result
        

    @patch("src.transform.initial_transform_handler.transform_tables")
    def test_transform_raises(self,t_tables,event):
       ##put in logs make, sure still raises
       t_tables.return_value = {}
       with pytest.raises(Exception) as e:
            result = lambda_handler({},{})


class TestTransform_table:
    def test_returns_dataframe(self, s3_with_bucket, event):
        table = "address"
        transforms = {"address":transform_location}
        response = transform_table("address", s3_with_bucket, TEST_BUCKET, TEST_KEY,transforms['address'])
        assert isinstance(response, pd.DataFrame)

class TestTransform_and_combine:
    @patch("src.transform.initial_transform_handler.load_json")
    def test_returns_dataframe(self,load_json, s3_with_bucket, event):
        table = "counterparty"
        transforms = Mock()
        transforms.return_value = pd.DataFrame() 
        secondary = pd.DataFrame()
        response = transform_and_combine(table, s3_with_bucket, TEST_BUCKET, TEST_KEY,"second_key",secondary,transforms)
        assert isinstance(response, pd.DataFrame)

class TestTransform_tables:
    @patch("src.transform.initial_transform_handler.transform_and_combine")
    @patch("src.transform.initial_transform_handler.transform_table")
    def test_returns_dict(self,counterparty,t_table,event):
        counterparty.return_value = pd.DataFrame()
        t_table.return_value = pd.DataFrame()
        timestamp = '2025-06-03 08:08:48.01'
        tables = event['tables']
        result = transform_tables(tables,"s3",timestamp)
        assert isinstance(result,dict)
    @patch("src.transform.initial_transform_handler.transform_and_combine")
    @patch("src.transform.initial_transform_handler.transform_table")
    def test_returns_all_tables(self,counterparty,t_table,event):
        counterparty.return_value = pd.DataFrame()
        t_table.return_value = pd.DataFrame()
        timestamp = '2025-06-03 08:08:48.01'
        tables = event['tables']
        result = transform_tables(tables,"s3",timestamp)
        
        assert "dim_counterparty" in result
        assert "dim_location" in result
    @patch("src.transform.initial_transform_handler.transform_and_combine")
    @patch("src.transform.initial_transform_handler.transform_table")
    def test_dict_values_is_dataframe(self,counterparty,t_table,event):
        counterparty.return_value = pd.DataFrame()
        t_table.return_value = pd.DataFrame()
        timestamp = '2025-06-03 08:08:48.01'
        tables = event['tables']
        result = transform_tables(tables,"s3",timestamp = '2025-06-03 08:08:48.01')
        
        assert isinstance(result["dim_counterparty"],pd.DataFrame)
        


class TestMake_key:
    def test_key_is_string(self):
        assert isinstance(make_key("table","2025"),str)
    def test_key_matches_expected(self):
        table = 'design'
        timestamp = '2025-06-03 08:08:48.01'
        key_design = "2025-06-03_08:08/design:2025-06-03_08:08:48.json"
       
        assert make_key(table,timestamp) == key_design
        
