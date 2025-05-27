import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

DYNAMO_REGION = 'us-east-1'
DYNAMO_TABLE = 'chat_threads'

def create_table():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=DYNAMO_REGION,
        endpoint_url=os.environ.get("DYNAMO_LOCAL_URL"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    try:
        table = dynamodb.create_table(
            TableName=DYNAMO_TABLE,
            KeySchema=[
                {'AttributeName': 'thread_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'thread_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        print(f"Tabela '{DYNAMO_TABLE}' criada com sucesso!")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Tabela '{DYNAMO_TABLE}' já existe.")
        else:
            raise

if __name__ == "__main__":
    create_table() 