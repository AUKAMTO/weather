import boto3
import os
import json
daynum = ""

client = boto3.Session(region_name='us-east-2').client('dynamodb')
def lambda_handler(event, context):
    daynum = event['queryStringParameters']['daynum']
        
    response = client.get_item(
        Key={
            'daynum': {'S': daynum}
        }, 
        TableName=os.environ["weatherDb"]
    )
    item = response['Item']
    # print(item)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps(item)
        }