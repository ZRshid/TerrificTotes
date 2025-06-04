import os
import botocore
import pytest
import pandas as pd
import boto3
from moto import mock_aws
from src.transform.load_json import load_json
from unittest.mock import patch

TEST_BUCKET = 'test-bucket'
TEST_TABLE = 'address'
TEST_JSON = """{
    "from_time": "2022-01-02 23:30:00.00", 
    "to_time": "2025-06-02 23:59:59.00", 
    "address": [
        {"address_id": 1, "address_line_1": "6826 Herzog Via", "address_line_2": null, "district": "Avon", "city": "New Patienceburgh", "postal_code": "28441", "country": "Turkey", "phone": "1803 637401", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"},
        {"address_id": 2, "address_line_1": "179 Alexie Cliffs", "address_line_2": null, "district": null, "city": "Aliso Viejo", "postal_code": "99305-7380", "country": "San Marino", "phone": "9621 880720", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}
    ]
}"""
TEST_KEY = "test/test.json"


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
            Body = TEST_JSON,
            Key = TEST_KEY
    )
    return s3

class TestLoadJson:
    def test_returns_dataframe(self,s3_with_bucket):
        s3 = s3_with_bucket
        result_df = load_json(TEST_BUCKET,TEST_KEY,TEST_TABLE,s3)
        assert isinstance(result_df, pd.DataFrame)

    def test_returns(self,s3_with_bucket):
        expected_columns = ["address_id", "address_line_1", "address_line_2", "district", "city", "postal_code", "country", "phone"]
        result_df = load_json(TEST_BUCKET,TEST_KEY,TEST_TABLE,s3_with_bucket)
        result_columns = result_df.columns.to_list()
        for expected in expected_columns:
            assert expected in result_columns

    def test_does_not_return_date_columns(self,s3_with_bucket):
        unwanted_columns = ['from_time','to_time']
        result_df = load_json(TEST_BUCKET,TEST_KEY,TEST_TABLE,s3_with_bucket)
        result_columns = result_df.columns.to_list()
        for expected in unwanted_columns:
            assert expected not in result_columns

    def test_raises_correctly(self,s3):
        #e.g no bucket
        with pytest.raises(botocore.exceptions.ClientError) as e:
            result_df = load_json(TEST_BUCKET,TEST_KEY,TEST_TABLE,s3)
        