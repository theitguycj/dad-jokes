# Import tools
import json
import boto3
from boto3.dynamodb.conditions import Key

# Get the service resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DYNAMO_DB_NAME')

# Function definition
def lambda_handler(event, context):
    
    # Pass in values from the Function URL
    emailLambda = event['queryStringParameters']['emailLambda']
    jokeLambda = event['queryStringParameters']['jokeLambda']
    
    # Query the last DB entry, extract the order number, and increment it by one
    response = table.query(
        KeyConditionExpression=Key('partition_needed').eq('jokepartition'),
        ScanIndexForward=False,
        Limit=1
    )
    
    #print(response['Items'][0]['order'])        #This is to check the DB query correctness.
    
    dbordernum = (response['Items'][0]['order'])
    newordernumber = dbordernum + 1
    
    # Convert URL values back for saving
    newJokeLambda = jokeLambda.replace("$$", " ")
    newEmailLambda = emailLambda.replace("$$", "+")
    
    # Insert into DynamoDB
    table.put_item(Item={
        "partition_needed": "jokepartition",
        "order": newordernumber,
        "email": newEmailLambda,
        "joke": newJokeLambda
    })
    
    # Return success message
    return {
        'statusCode': 200,
        'body': json.dumps(emailLambda)
    }