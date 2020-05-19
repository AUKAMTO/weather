import boto3
import os
import json
daynum = ""

client = boto3.Session(region_name='us-east-2').client('dynamodb')
def lambda_handler(event, context):
    daynum = event['queryStringParameters']['daynum']
    startTime = event['queryStringParameters']['startTime']
    endTime = event['queryStringParameters']['endTime']
    daynum = 0
    startTime = 0
    endTime = 0

        
    response = client.query(
        TableName=os.environ["weatherDb"],
        KeyConditionExpression='daynum = :daynum AND inputtime BETWEEN :songval1 AND :songval2',
        ExpressionAttributeValues={
            ':daynum': {'S': daynum},
            ':songval1': {'S': startTime},
            ':songval2': {'S': endTime}
        }
    )
    items = response['Items']
    # print(item)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps(items)
        }