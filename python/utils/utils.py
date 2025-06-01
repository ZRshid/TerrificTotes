import boto3
from botocore.exceptions import ClientError
import json
import logging 

def get_secret(secrets_name:str):
    """
    Get a secret from AWS Secrets Manager.
    Args:
        secret_name (str): The name of the secret you want to get.
    Returns:
        dict: The secret data as a dictionary.
        None: If there was an error getting the secret.
    """
    secrets_manager = boto3.client('secretsmanager')
    try:
        response=secrets_manager.get_secret_value(SecretId=secrets_name)
        secret_dict = json.loads(response['SecretString'])
        logging.info(f"Secret: {secrets_name} retrieved")
        return secret_dict
    except ClientError as e:
        logging.error(f"The following error has occurred: {e}") # logging error - does it go to Cloudwatch and trigger error?
        raise e