from python.utils.utils import get_secret
import os  
import boto3
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

@pytest.fixture
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
    
        result = get_secret(secret_name)

        assert result == expected_secret
    



    # def test_creates_secret(self,mock_secrets_manager):
    #     expected_name = "My_test_secret"
    #     expected_secret = '{"user_id": "my_user", "password": "my_password"}'



    #     results = store_secret(mock_secrets_manager,
    #                           user_id="my_user",
    #                           password="my_password",
    #                           name=expected_name)
    #     response = mock_secrets_manager.get_secret_value(SecretId=expected_name)
    #     pprint(response)
    #     assert response['SecretString'] == expected_secret
    #     assert response["Name"] == expected_name
    #     assert response['ResponseMetadata']['HTTPStatusCode'] == 200











