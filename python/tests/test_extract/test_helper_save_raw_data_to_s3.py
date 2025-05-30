from moto import mock_aws
import os
import boto3
import pytest
import json
import re
from python.src.extract.helper_save_raw_data_to_s3 import save_raw_data_to_s3


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_aws():
        yield boto3.client('s3', region_name='eu-west-2')

@pytest.fixture(autouse=True)
def bucket(s3):
    s3.create_bucket(
        Bucket='test_bucket',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

@pytest.fixture(autouse=True)
def raw_data():
    data =  [{"id": 1, "name": "Alice", "email": "alice@example.com", "active": True},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "active": False}]
    return json.dumps(data)

class TestSaveRawDataToS3:
    def test_raw_data_bucket_is_not_empty(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test_bucket")
        response = s3.list_objects_v2(
            Bucket = "test_bucket"
        )
        assert len(response.get("Contents", [])) > 0 

    def test_raw_data_bucket_contains_folders_with_timestamp(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test_bucket")
        response = s3.list_objects_v2(
            Bucket = "test_bucket"
        )
        # regex pattern for matching timestamp format: 2025-05-29_23:14
        pattern = r"20\d{2}-[01][0-9]-[0-3][0-9]_[012][0-9]:[0-5][0-9]"
        folders = [re.fullmatch(pattern, item["Key"].split("/")[0]) for item in response["Contents"]]
        assert all(folders)

    def test_raw_data_bucket_contains_json_files(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test_bucket")
        response = s3.list_objects_v2(
            Bucket = "test_bucket"
        )
        file_ends = [item["Key"].endswith(".json") for item in response["Contents"]]
        assert all(file_ends)

    def test_raw_data_bucket_contains_files_with_timestamp(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test_bucket")
        response = s3.list_objects_v2(
            Bucket = "test_bucket"
        )
        # regex pattern for matching timestamp format: 2025-05-29_23:14:02
        pattern = r"20\d{2}-[01][0-9]-[0-3][0-9]_[012][0-9]:[0-5][0-9]:[0-5][0-9]"
        files = [re.search(pattern, item["Key"].split("/")[-1]) for item in response["Contents"]]
        assert all(files)
    
    def test_raw_data_bucket_contains_files_with_table_name(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test_bucket")
        response = s3.list_objects_v2(
            Bucket = "test_bucket"
        )
        files = [item["Key"].split("/")[-1] for item in response["Contents"]]
        assert all("test_table" in file for file in files)

    def test_raw_data_bucket_contains_files_with_correct_content(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test_bucket")
        response = s3.list_objects_v2(
            Bucket = "test_bucket"
        )
        for item in response["Contents"]:
            file = s3.get_object(
                Bucket = "test_bucket", 
                Key = item["Key"]
            )
            content = file['Body'].read().decode('utf-8')
            assert content == raw_data

    def test_save_raw_data_to_s3_raises_exception_on_error(self, s3):
        with pytest.raises(Exception) as error_message:
            save_raw_data_to_s3(["random_data"], "test_table", "test_bucket")
        assert "Error uploading to S3" in str(error_message.value)
