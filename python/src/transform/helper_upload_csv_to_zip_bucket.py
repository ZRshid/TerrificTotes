import boto3
from botocore.exceptions import BotoCoreError, ClientError

def upload_csv_to_zip_bucket(local_path, bucket_name, s3_key):
        s3 = boto3.client("s3")
        try:
            s3.upload_file(local_path, bucket_name, s3_key)
            return "File has been uploaded in the zip bucket"
        except (BotoCoreError, ClientError) as error:
              return f"Upload failed"