import boto3
from botocore.exceptions import ClientError
import json
import logging
from datetime import datetime


def get_secret(secrets_name: str):
    """
    Get a secret from AWS Secrets Manager.
    Args:
        secret_name (str): The name of the secret you want to get.
    Returns:
        dict: The secret data as a dictionary.
        None: If there was an error getting the secret.
    """
    secrets_manager = boto3.client("secretsmanager")
    try:
        response = secrets_manager.get_secret_value(SecretId=secrets_name)
        secret_dict = json.loads(response["SecretString"])
        logging.info(f"Secret: {secrets_name} retrieved")
        return secret_dict
    except ClientError as e:
        # logging error - does it go to Cloudwatch and trigger error?
        logging.error(f"The following error has occurred: {e}")
        raise e


def datetime_to_str(dt: datetime) -> str:
    """Convert a datetime to the string format we are using

    Args:
        dt (datetime): a datetime

    Returns:
        str: A string in the format: %Y-%m-%d %H:%M:%S.%f, except seconds only
        have 3 decimal places.
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
