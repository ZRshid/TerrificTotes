from src.load.load import get_secret, download_parquet_from_s3_and_saves_it_in_memory, convert_buffer_to_dataframe
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import boto3
import os 
import io 
from botocore.exceptions import ClientError
from moto import mock_aws 
import pytest 
import json


@pytest.fixture()  
def aws_credentials():
    '''Mocked AWS Credentials for moto'''
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

# @pytest.fixture()
# def mock_secrets_manager(aws_credentials): 
#     with mock_aws():
#         client = boto3.client('secretsmanager')
#         yield client

@pytest.fixture()
def mock_s3_boto():
    """Create an S3 boto3 client and return the client object"""
    with mock_aws():
        client = boto3.client('s3', region_name='eu-west-2')
        yield client

@pytest.fixture()
def mock_s3_bucket(mock_s3_boto):
     bucket = "testbucket"
     key = "testkey"
     body = "testing"
     mock_s3_boto.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
     mock_s3_boto.put_object(Bucket=bucket, Key=key, Body=body)
     return bucket, key, body

# class TestGetSecret:
#     def test_get_secret_returns_expected_secret(self, mock_secrets_manager):
#         secret_name = "test_datawarehouse"
#         expected_secret = {
#             'username': 'test_user',
#             'password': 'fake_password',
#             'engine': 'postgres',   
#             'host': 'localhost',
#             'port': 5432
#         }
#         response = mock_secrets_manager.create_secret(
#             Name = secret_name, 
#             SecretString = json.dumps(expected_secret)
#             )
#         result = get_secret(secret_name)
#         assert result == expected_secret
#         assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    # def test_get_secret_raises_an_error_when_secret_does_not_exist(self):
    #     missing_secret_name = "nonexistent_secret"
    #     with pytest.raises(ClientError):
    #         get_secret(missing_secret_name)


class TestDownloadingParquetFromS3():
    def test_downloads_parquest_file_from_an_s3_bucket_into_IoBytes(self, mock_s3_boto,mock_s3_bucket):
        bucket, key , body = mock_s3_bucket
        result = download_parquet_from_s3_and_saves_it_in_memory(bucket, key)
        print(result)
        assert isinstance(result,io.BytesIO)

    def test_checks_the_content_inside_the_bytes(self, mock_s3_boto,mock_s3_bucket):
        bucket, key, body = mock_s3_bucket
        result = download_parquet_from_s3_and_saves_it_in_memory(bucket, key)
        content = result.read()
        assert content == body.encode()
       
class TestConvertingParquetToDataframe():
     def test_converts_parquet_into_a_dataframe(self):
        df = pd.DataFrame([
        {
            "design_id": 8,
            "created_at": "2022-11-03 14:20:49.962000",
            "design_name": "Wooden",
            "file_location": "/usr",
            "file_name": "wooden-20220717-npgz.json",
            "last_updated": "2022-11-03 14:20:49.962000"
        }
    ])
        table = pa.Table.from_pandas(df)
        buffer = io.BytesIO()
        pq.write_table(table, buffer)
        buffer.seek(0) 
        result = convert_buffer_to_dataframe(buffer)
        pd.testing.assert_frame_equal(df, result)
        assert result.shape == (1,6)  
      
       

        
    
    
 


           



