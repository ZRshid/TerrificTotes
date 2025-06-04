from src.transform.to_parquet import to_parquet
import pytest
import pandas as pd
from moto import mock_aws
import boto3
import os
import re
import awswrangler as wr
from pandas.testing import assert_frame_equal

@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

@pytest.fixture(scope='function')
def s3():
    with mock_aws():
        yield boto3.client('s3', region_name='eu-west-2')

@pytest.fixture(scope='function', autouse=True)
def bucket(s3):
    s3.create_bucket(
        Bucket='test-bucket',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

@pytest.fixture(autouse=True)
def dataframe():
    df_test = pd.DataFrame({'key': [1, 2], 'key2': [2, 3]})
    return df_test

class TestToParquet:
    def test_parquet_file_saved_to_bucket(self, s3, dataframe):
        to_parquet(dataframe, "test-bucket", "test")
        response = s3.list_objects_v2(
            Bucket = "test-bucket"
        )
        print(response)
        assert len(response.get("Contents", [])) > 0

    def test_raw_data_bucket_contains_parquet_files(self, s3, dataframe):
        to_parquet(dataframe, "test-bucket", "test")
        response = s3.list_objects_v2(
            Bucket = "test-bucket"
        )
        file_ends = [item["Key"].endswith(".parquet") for item in response["Contents"]]
        assert all(file_ends)

    def test_raw_data_bucket_contains_files_with_timestamp(self, s3, dataframe):
        to_parquet(dataframe, "test-bucket", "test")
        response = s3.list_objects_v2(
            Bucket = "test-bucket"
        )
        # regex pattern for matching timestamp format: 2025-05-29_23:14:02
        pattern = r"20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])_([01]\d|2[0-3]):([0-5]\d|60):([0-5]\d|60)"
        
        files = [re.search(pattern, item["Key"].split("/")[-1]) for item in response["Contents"]]
        assert all(files)

    def test_raw_data_bucket_contains_files_with_correct_content(self, s3, dataframe):
        to_parquet(dataframe, "test-bucket", "test")
        response = s3.list_objects_v2(
            Bucket = "test-bucket"
        )
        key = [data["Key"] for data in response.get("Contents", [])]
        for parquet in key:
            path = f"s3://test-bucket/test"
            content = wr.s3.read_parquet(path)
        assert_frame_equal(content, dataframe, check_dtype=False)