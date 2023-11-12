import json
import boto3
import os

def validate_request_body(request_body):
    expected_schema = {'ProductID', 'Count'}

    if set(request_body.keys()) != expected_schema:
        raise ValueError('Invalid request body. Unexpected fields.')

def update_stock(event, context):
    try:
        body = json.loads(event['Records'][0]['body'])

        validate_request_body(body)

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.getenv("UPDATE_PRODUCT_INFO_TABLE_NAME"))

        item = body
        response =  table.put_item(Item=item)

        print("Updated Successfully")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Item {response} updated successfully.'})
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
