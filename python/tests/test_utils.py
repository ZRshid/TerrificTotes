from python.utils.utils import get_secret
import os  
import boto3
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

@pytest.fixture()
def mock_secrets_manager(aws_credentials): # check this: why aws_credentials is not accessed.
    with mock_aws():
        client = boto3.client('secretsmanager')
        yield client


class TestGetSecret:
    
    def test_get_secret_returns_expected_secret(self, mock_secrets_manager):
        secret_name = "test_secret"
        expected_secret = {
            'username': 'test_user',
            'password': 'fake_password',
            'engine': 'postgres',   
            'host': 'localhost',
            'port': 5432
        }

        response = mock_secrets_manager.create_secret(Name = secret_name, SecretString = json.dumps(expected_secret))

        result = get_secret(secret_name)

        assert result == expected_secret
    
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200


    def test_wrong_secrets(self, mock_secrets_manager):
        missing_secret_name = "nonexistent_secret"
        with pytest.raises(ClientError) as err:
            mock_secrets_manager.get_secret_value(SecretId=missing_secret_name)






