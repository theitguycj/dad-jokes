# Import tools
import json
import boto3
from boto3.dynamodb.conditions import Key
import os

# Get the service resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DYNAMO_DB_NAME')
ses = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    
    # Query table for the latest order #, joke, and email address (This is the user's joke)
    response = table.query(
        KeyConditionExpression=Key('partition_needed').eq('jokepartition'),
        ScanIndexForward=False,
        Limit=1
    )
    
    order1 = (response['Items'][0]['order'])
    joke1 = (response['Items'][0]['joke'])
    userEmail = (response['Items'][0]['email'])
    
    #print("The number " + str(order1) + " joke is '" + str(joke1) + "'")           #Won't need but I'll keep for future reference.
    
    # If/Else statements to run script
    if str(userEmail) == "":                     # JSON response to email address being absent
        return {
            'statusCode': 404,
            'body': json.dumps('This record had no email address.')
        }
    
    else:                                   # Email address is present
        # Query DynamoDB using "less than" for the sort key to get the 5 jokes before the last one
        response = table.query(
            KeyConditionExpression=Key('partition_needed').eq('jokepartition') & Key('order').lt(order1),
            ScanIndexForward=False,
            Limit=5
        )
    
        # Save the 5 previous jokes to be emailed (Use print(response*) for TESTING)
        joke2 = (response['Items'][0]['joke'])
        joke3 = (response['Items'][1]['joke'])
        joke4 = (response['Items'][2]['joke'])
        joke5 = (response['Items'][3]['joke'])
        joke6 = (response['Items'][4]['joke'])
    
        # Email the jokes to user
        emailResponse = ses.send_email(
            Destination = {
                'ToAddresses': ['ENTER_YOUR_EMAIL_ADDRESS_HERE']
            },
            Message = {
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': 'This is your joke: ' + joke1 + '\t\n \t\nAnd here are the previous 5 jokes:' '\t\n \t\nJoke 1: ' + joke6 + '\t\nJoke 2: ' + joke5 + '\t\nJoke 3: ' + joke4 + '\t\nJoke 4: ' + joke3 + '\t\nJoke 5: ' + joke2,
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Your dad jokes are here!',
                },
            },
        
            Source='ENTER_YOUR_EMAIL_ADDRESS_HERE'
        )
        
        # JSON response to success
        return {
            'statusCode': 200,
            'body': json.dumps('This has worked!')
        }
