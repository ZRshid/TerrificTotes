import pytest
import json
import os
from unittest.mock import patch
from moto import mock_aws
from python.src.extract.extract_handler import lambda_handler

## extract one table and save it to the raw data bucket

# mock/patch logging - returns a log - message info

# test if the log returns what we expect


# test if lambda returns list of tables uploaded
@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture()
def event():
    return """{"tables" : ["table_name"],
                "from_time" : "2025-06-02 11:30:55.00",
                 "to_time" : "2025-06-02 11:31:55.00", "raw_data_bucket" : "tt-raw-data"
                 }"""


@pytest.fixture()
def event_tables():
    return """{"tables" : ["table_name","sales"],
                "from_time" : "2025-06-02 11:30:55.00",
                 "to_time" : "2025-06-02 11:31:55.00", "raw_data_bucket" : "tt-raw-data"
                 }"""


@pytest.fixture()
def row():
    return ["field1", "field2"]


@pytest.fixture()
def columns():
    return [{"name": "column1"}, {"name": "column2"}]


# @pytest.fixture()
# def context():
# @pytest.fixture()
# def mock_secrets_manager(aws_credentials):
#     with mock_aws():
#         client = boto3.client('')
#         yield client


@patch("python.src.extract.extract_handler.save_raw_data_to_s3")
@patch("python.src.extract.extract_handler.close_db")
@patch("python.src.extract.extract_handler.connect_to_db")
@patch("python.src.extract.extract_handler.query_db")
class TestLambdaHandler:

    def test_lambda_handler_returns_dict(
        self, query_db_mm, b, c, d, event, row, columns
    ):
        query_db_mm.return_value = ([row], columns)
        result = lambda_handler(event, {})

        assert isinstance(result, dict)
        # assert isinstance(result[])

    def test_lambda_handler_returned_dict_keys_matching(
        self, query_db_mm, b, c, d, event, row, columns
    ):
        query_db_mm.return_value = ([row], columns)

        expected_keys = "tables"

        result = lambda_handler(event, {})

        assert expected_keys in result

    def test_lambda_handler_returns_dict_lists(
        self, query_db_mm, b, c, d, event, row, columns
    ):
        query_db_mm.return_value = ([row], columns)

        result = lambda_handler(event, {})

        assert isinstance(result["tables"], list)

    # test extract and returns one table

    def test_lambda_handler_extracts_and_return_one_table(
        self, query_db_mm, connect_db, close_db, save_s3, event, row, columns
    ):
        query_db_mm.return_value = ([row], columns)
        expected_result = ["table_name"]

        result = lambda_handler(event, {})

        assert result == {"tables": ["table_name"]}

    # # test extract and returns two tables

    def test_lambda_handler_extracts_and_return_two_tables(
        self, query_db_mm, connect_db, close_db, save_s3, event_tables, row, columns
    ):
        query_db_mm.return_value = ([row], columns)
        expected_result = ["table_name"]

        result = lambda_handler(event_tables, {})

        assert result == {"tables": ["table_name", "sales"]}


# test if the data have been saved
