from src.transform.helper_upload_csv_to_zip_bucket import upload_csv_to_zip_bucket
import pytest
import boto3
from unittest.mock import patch 
from botocore.exceptions import BotoCoreError, ClientError

class Test_upload_csv_to_zip_bucket():

    # I need to mock a client request to upload my file to my bucket
    # I need to patch the client
    @patch("boto3.client")
    def test_func_uploads_file_to_s3(self, mock_boto3_client):
        mock_s3 = mock_boto3_client.return_value
        local_path = "Data/currency-codes.csv"
        bucket_name = "zip-bucket"
        s3_key = "s3_currency_codes.csv" # full path and filename of an object within a bucket

        result = upload_csv_to_zip_bucket(local_path, bucket_name, s3_key)
        # https://docs.python.org/3/library/unittest.mock.html
        #checks if the mock upload file has been called 
        
        mock_s3.upload_file.assert_called_with(local_path, bucket_name, s3_key)
        
        assert result == "File has been uploaded in the zip bucket"


    #https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
    @patch("boto3.client")
    def test_upload_csv_to_zip_bucket_error(self, mock_boto3_client):
        mock_s3 = mock_boto3_client.return_value

        # fake client response
        error_response = {"Error": {"Message": "Upload failed"}}
        exception = ClientError(error_response, "UploadFile")

    # Configure the mock to raise this error when upload_file is called
        mock_s3.upload_file.side_effect = exception

        local_path = "Data/currency-codes.csv"
        bucket_name = "zip-bucket"
        s3_key = "s3_currency_codes.csv"

    
        result = upload_csv_to_zip_bucket(local_path, bucket_name, s3_key)

        # Check that the error message is included in the result
        assert "Upload failed" in result
