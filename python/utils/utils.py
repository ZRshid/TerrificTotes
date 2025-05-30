import boto3
from botocore.exceptions import ClientError
from pprint import pprint
import json
import logging 



def get_secret(secrets_name):
    secrets_manager = boto3.client('secretsmanager')
    try:
        response=secrets_manager.get_secret_value(SecretId=secrets_name)
        secret_dict = json.loads(response['SecretString'])
        return secret_dict
    except ClientError as e:
        logging.error(f"The following error has occurred {e}") # logging error - does it go to Cloudwatch and trigger error?

pprint(get_secret("totesys_secret")) 






