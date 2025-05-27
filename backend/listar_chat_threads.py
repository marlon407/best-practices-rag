import boto3
import os

from dotenv import load_dotenv 
load_dotenv()

DYNAMO_REGION = 'us-east-1'
DYNAMO_TABLE = 'chat_threads'


if os.environ.get("DYNAMO_LOCAL") == "1":
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=DYNAMO_REGION,
        endpoint_url=os.environ.get("DYNAMO_LOCAL_URL"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
else:
    dynamodb = boto3.resource('dynamodb', region_name=DYNAMO_REGION)

table = dynamodb.Table(DYNAMO_TABLE)

response = table.scan()
items = response.get('Items', [])

for item in items:
    print(item) 