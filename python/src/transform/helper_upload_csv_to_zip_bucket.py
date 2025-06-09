import boto3
import sys
from botocore.exceptions import BotoCoreError, ClientError

FAILURE_MESSAGE = "Upload failed"
SUCCESS_MESSAGE = "File has been uploaded in the zip bucket"

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
            return SUCCESS_MESSAGE
        except (BotoCoreError, ClientError) as error:
              return FAILURE_MESSAGE+f": {error}"
        
def main(*args):
    result = upload_csv_to_zip_bucket(*args) #should raise error if arguments does not hold 3
    print(result)
    if result == SUCCESS_MESSAGE:
        print("success")
        exit(0)
    else:
        exit(1)

#If runing as the main script load commandline arguements to use in the function
if __name__ == "__main__":
      commandline_args = sys.argv[1:4] #0 is this file, so need 1,2, and 3. igonore anymore
      main(*commandline_args)