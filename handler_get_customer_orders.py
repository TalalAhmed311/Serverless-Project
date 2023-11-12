import boto3
import os

def get_customer_orders(event, context):
    try:
        table_name = os.getenv("CUSTOMER_ORDERS_TABLE_NAME")

        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table(table_name)
        response = table.scan()
        items = response['Items']

        return {
            'statusCode': 200,
            'body': items
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'error': 'Internal Server Error',
                'message': str(e)
            }
        }
