import boto3
import time
from typing import List, Tuple
from boto3.dynamodb.conditions import Key
import os

# Ajuste a região conforme necessário
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

def save_message(thread_id: str, question: str, answer: str):
    table.put_item(
        Item={
            'thread_id': thread_id,
            'timestamp': int(time.time() * 1000),  # milissegundos
            'question': question,
            'answer': answer
        }
    )

def get_thread_history(thread_id: str) -> List[Tuple[str, str]]:
    response = table.query(
        KeyConditionExpression=Key('thread_id').eq(thread_id),
        ScanIndexForward=True  # ordem crescente
    )
    return [(item['question'], item['answer']) for item in response.get('Items', [])]  