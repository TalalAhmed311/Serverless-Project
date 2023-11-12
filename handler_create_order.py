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

def create_orders(event, context):
    try:
        request_body = json.loads(event['body'])
        
        validate_request_body(request_body)

        queue_name = os.getenv("CUSTOMER_ORDERS_QUEUE_NAME")
        queue_url = get_queue_url(queue_name)

        response = send_message_to_sqs(request_body, queue_url)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order created successfully!',
                'sqsResponse': response
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
