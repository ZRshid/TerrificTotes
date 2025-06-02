from moto import mock_aws
import os
import boto3
import pytest
import json
import re
from python.src.extract.helper_save_raw_data_to_s3 import save_raw_data_to_s3


@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3():
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-2")


@pytest.fixture(scope="function", autouse=True)
def bucket(s3):
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
    )


@pytest.fixture(autouse=True)
def raw_data():
    data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "active": True},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "active": False},
    ]
    return json.dumps(data)


class TestSaveRawDataToS3:
    def test_raw_data_bucket_is_not_empty(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test-bucket")
        response = s3.list_objects_v2(Bucket="test-bucket")
        assert len(response.get("Contents", [])) > 0

    def test_raw_data_bucket_contains_folders_with_timestamp(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test-bucket")
        response = s3.list_objects_v2(Bucket="test-bucket")
        # regex pattern for matching timestamp format: 2025-05-29_23:14
        pattern = r"20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])_([01]\d|2[0-3]):([0-5]\d|60)"

        folders = [
            re.fullmatch(pattern, item["Key"].split("/")[0])
            for item in response["Contents"]
        ]
        assert all(folders)

    def test_raw_data_bucket_contains_json_files(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test-bucket")
        response = s3.list_objects_v2(Bucket="test-bucket")
        file_ends = [item["Key"].endswith(".json") for item in response["Contents"]]
        assert all(file_ends)

    def test_raw_data_bucket_contains_files_with_timestamp(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test-bucket")
        response = s3.list_objects_v2(Bucket="test-bucket")
        # regex pattern for matching timestamp format: 2025-05-29_23:14:02
        pattern = r"20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])_([01]\d|2[0-3]):([0-5]\d|60):([0-5]\d|60)"

        files = [
            re.search(pattern, item["Key"].split("/")[-1])
            for item in response["Contents"]
        ]
        assert all(files)

    def test_raw_data_bucket_contains_files_with_table_name(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test-bucket")
        response = s3.list_objects_v2(Bucket="test-bucket")
        files = [item["Key"].split("/")[-1] for item in response["Contents"]]
        assert all("test_table" in file for file in files)

    def test_raw_data_bucket_contains_files_with_correct_content(self, s3, raw_data):
        save_raw_data_to_s3(raw_data, "test_table", "test-bucket")
        response = s3.list_objects_v2(Bucket="test-bucket")
        for item in response["Contents"]:
            file = s3.get_object(Bucket="test-bucket", Key=item["Key"])
            content = file["Body"].read().decode("utf-8")
            assert content == raw_data

    def test_save_raw_data_to_s3_raises_TypeError(self):
        with pytest.raises(TypeError):
            save_raw_data_to_s3(["random_data"], "test_table", "test-bucket")

    def test_save_raw_data_to_s3_raises_exception_on_error(self):
        with pytest.raises(Exception):
            save_raw_data_to_s3("random_data", "test_table", 90)
