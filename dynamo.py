import boto3
from boto3.dynamodb.conditions import Key


def create_bunch_of_users():
    dynamodb = boto3.resource('dynamodb',aws_access_key_id="",
         aws_secret_access_key="", region_name='us-east-1')

    table = dynamodb.Table('my-data')

    for n in range(3):
        table.put_item(Item={
            'userId': str(n),
            'first_name': 'Jon',
            'last_name': 'Doe' + str(n),
            'email': 'jdoe' + str(n) + '@test.com'
        })

# create_bunch_of_users()


def scan_first_and_last_names():
    dynamodb = boto3.resource('dynamodb', aws_access_key_id="",
                              aws_secret_access_key="", region_name='')

    table = dynamodb.Table('my-data')

    resp = table.scan(ProjectionExpression="first_name, last_name")

    print(resp['Items'])

scan_first_and_last_names()


def multi_part_scan():
    dynamodb = boto3.resource('dynamodb', aws_access_key_id="",
                              aws_secret_access_key="", region_name='')

    table = dynamodb.Table('my-data')

    response = table.scan()
    result = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        result.extend(response['Items'])

multi_part_scan()