import boto3
import time
from typing import List, Tuple
from boto3.dynamodb.conditions import Key
import os

# Ajuste a região conforme necessário
DYNAMO_REGION = 'us-east-1'
DYNAMO_TABLE = 'chat_threads'

def init_dynamodb():
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
    
    # Verifica se a tabela existe
    try:
        dynamodb.Table(DYNAMO_TABLE).table_status
        print(f"Tabela {DYNAMO_TABLE} já existe")
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        print(f"Criando tabela {DYNAMO_TABLE}...")
        table = dynamodb.create_table(
            TableName=DYNAMO_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'thread_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'thread_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # Espera a tabela ficar ativa
        table.meta.client.get_waiter('table_exists').wait(TableName=DYNAMO_TABLE)
        print(f"Tabela {DYNAMO_TABLE} criada com sucesso!")
    
    return dynamodb.Table(DYNAMO_TABLE)

# Inicializa a tabela
table = init_dynamodb()

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