import json
import boto3
import os

def send_message_to_sqs(message_body, queue_url):
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_body)
    )
    return response

def get_queue_url(queue_name):
    sqs = boto3.client('sqs')
    response = sqs.get_queue_url(
        QueueName=queue_name
    )
    return response['QueueUrl']

def validate_request_body(request_body):
    expected_schema = {'CustomerID', 'ProductID', 'Count'}

    if set(request_body.keys()) != expected_schema:
        raise ValueError('Invalid request body. Unexpected fields.')
    
def process_order(event, context):
    try:
        item = json.loads(event["Records"][0]['body'])
        
        validate_request_body(item)

        table_name = os.getenv("CUSTOMER_ORDERS_TABLE_NAME")

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=item)

        queue_name = os.getenv("PROCESS_ORDERS_QUEUE_NAME")

        queue_url = get_queue_url(queue_name)
        message_item = {
            "ProductID": item["ProductID"],
            "Count": item["Count"]
        }
        response_sqs = send_message_to_sqs(message_item, queue_url)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order created successfully!',
                'sqsResponse': response_sqs
            })
        }
    
    except ValueError as ve:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Bad Request',
                'message': str(ve)
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            })
        }
