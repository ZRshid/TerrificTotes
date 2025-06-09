from src.transform.initial_transform_handler import lambda_handler, transform_table
from src.transform.transform_location import transform_location
import pytest
import boto3
from moto import mock_aws
import pandas as pd
import os
from unittest.mock import patch
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
    def test_lambda_handler_returns_dict(self):
        pass

    def test_dict_contains_keys(self):
        expected_keys = ["transformed_tables","timestamp"]
        
        pass


    def test_transform_raises(self):
       ##put in logs make, sure still raises
       with pytest.raises(Exception) as e:
           ...

class TestTransform_Table:
    def test_returns_dataframe(self, s3_with_bucket, event):
        table = "address"
        transforms = {"address":transform_location}
        transformed_tables = []
        response = transform_table("address", s3_with_bucket, transformed_tables, TEST_BUCKET, TEST_KEY,transform_location)
        assert isinstance(response, pd.DataFrame)

    def test_added_to_transformed_tables(self, s3_with_bucket, event):
        table = "address"
        transforms = {"address":transform_location}
        transformed_tables = []
        response = transform_table("address", s3_with_bucket, transformed_tables, TEST_BUCKET, TEST_KEY,transform_location)
        assert table in transformed_tables

class TestOther:
    ...

class TestMake_key:
    def test_key_is_string():
        assert isinstance(Make_key("table","2025"),str)
    def test_key_matches_expected():
        table = 'design'
        timestamp = '2025-05-05 23:11:23:48.01'
        expected = ??
        
