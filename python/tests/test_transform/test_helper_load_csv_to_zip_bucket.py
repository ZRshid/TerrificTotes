from src.transform.helper_upload_csv_to_zip_bucket import upload_csv_to_zip_bucket, main
import pytest
import boto3
from unittest.mock import patch 
from botocore.exceptions import BotoCoreError, ClientError

# Test class for the upload_csv_to_zip_bucket function
class Test_upload_csv_to_zip_bucket():
    
    @patch("boto3.client")
    def test_func_uploads_file_to_s3(self, mock_boto3_client):
        # Mock the boto3 S3 client
        mock_s3 = mock_boto3_client.return_value

        # Define test input values
        local_path = "Data/currency-codes.csv"
        bucket_name = "zip-bucket" 
        s3_key = "s3_currency_codes.csv"  # Object key in the S3 bucket

        # Call the function under test and capture the result
        result = upload_csv_to_zip_bucket(local_path, bucket_name, s3_key)
        
        # Verify that the mocked upload_file method was called with the correct arguments
        mock_s3.upload_file.assert_called_with(local_path, bucket_name, s3_key)

         # Check that the function returns the expected success message
        assert result == "File has been uploaded in the zip bucket"


   
    @patch("boto3.client")
    def test_upload_csv_to_zip_bucket_error(self, mock_boto3_client):
        # Mock the boto3 S3 client
        mock_s3 = mock_boto3_client.return_value

        # Simulate a ClientError when upload_file is called
        error_response = {"Error": {"Message": "Upload failed"}}
        exception = ClientError(error_response, "UploadFile")
        mock_s3.upload_file.side_effect = exception

        # Define test input values
        local_path = "Data/currency-codes.csv"
        bucket_name = "zip-bucket"
        s3_key = "s3_currency_codes.csv"

        # Call the function under test and capture the result
        result = upload_csv_to_zip_bucket(local_path, bucket_name, s3_key)

        # Verify that the error message is included in the function's output
        assert "Upload failed" in result

class TestMain():

    def test_main_raise_typeerror_without_args(self):
        
        args = ()
        with pytest.raises(TypeError) as e:
            main(*args)
    @patch("boto3.client")       
    def test_main_exits_with_code_0(self,boto3):
        local_path = ""
        bucket_name = ""
        s3_key = ""
        with pytest.raises(SystemExit) as e:
            main(local_path,bucket_name,s3_key)
            assert e.type == SystemExit
            assert e.value.code == 0
    @patch("src.transform.helper_upload_csv_to_zip_bucket.boto3.client") 
    def test_main_exits_with_code_1_with_fail(self,s3):
        local_path = ""
        bucket_name = ""
        s3_key = ""
        s3().upload_file.side_effect = BotoCoreError()
        with pytest.raises(SystemExit) as e:
            main(local_path,bucket_name,s3_key)
        assert e.type == SystemExit
        assert e.value.code == 1
            
