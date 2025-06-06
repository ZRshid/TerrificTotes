import boto3
from botocore.exceptions import BotoCoreError, ClientError

def upload_csv_to_zip_bucket(local_path, bucket_name, s3_key):
        """
        Uploads a CSV file to a specified S3 bucket and key.

        Args:
            local_path (str): The local file path of the CSV file to be uploaded.
            bucket_name (str): The name of the S3 bucket where the file will be uploaded.
            s3_key (str): The S3 key (path within the bucket) where the file will be stored.

        Returns:
            str: A message indicating whether the upload was successful or failed.

        Raises:
            BotoCoreError: If there is an error with the boto3 core functionality.
            ClientError: If there is an error with the S3 client during the upload process.
        """
        s3 = boto3.client("s3")
        try:
            s3.upload_file(local_path, bucket_name, s3_key)
            return "File has been uploaded in the zip bucket"
        except (BotoCoreError, ClientError) as error:
              return f"Upload failed"