from flask import Flask
import os
import boto3
import botocore
from flask import request, jsonify
from dotenv import load_dotenv
load_dotenv()
import time
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import uuid
import random
import threading
import re
from pymongo import MongoClient
import json


class EmailNotValidError(Exception):
    """Raised when the email is not valid"""
    pass


class ExportingThread(threading.Thread):
    def __init__(self):
        self.progress = 0
        self.output = None
        super().__init__()

    def run(self):
        # Your exporting stuff goes here ...
        for _ in range(10):
            time.sleep(1)
            self.progress += 10
        self.output = "Summary of this document"


exporting_threads = {}


def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

# if we hav e.aws/credentials and .aws/config stroed in our system then
# we don't need to pass aws access key, secret key and region


s3_resource = boto3.resource('s3')


def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    print(current_region)
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name)
    print(bucket_name, current_region)
    return bucket_name, bucket_response


# create_bucket("romil", s3_resource)

def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name


def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)


client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION'))

dynamodb = boto3.resource('dynamodb',aws_access_key_id="",
         aws_secret_access_key="", region_name=os.getenv('COGNITO_REGION'))
# print(list(dynamodb.tables.all()))
my_data_table = dynamodb.Table('my-data')

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.flask_db
todos = db.todos

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()


def validate_user(access_token):
    response = client.get_user(
        AccessToken=access_token
    )
    return response


@app.route("/", methods=['GET'])
def hello():
    return "Hello, World!"


def delete_all_objects(bucket_name):
    res = []
    bucket=s3_resource.Bucket(bucket_name)
    for obj_version in bucket.object_versions.all():
        res.append({'Key': obj_version.object_key,
                    'VersionId': obj_version.id})
    print(res)
    bucket.delete_objects(Delete={'Objects': res})


@app.route("/upload-s3", methods=['post'])
def upload_s3():
    try:
        first_file_name = create_temp_file(300, 'firstfile.txt', 'f')
        first_object = s3_resource.Object(
            bucket_name="new-files-uploads-data", key=first_file_name)
        first_object.upload_file(first_file_name, ExtraArgs={
                          'ACL': 'public-read'})
        # download from s3
        s3_resource.Object("new-files-uploads-data", first_file_name).download_file('first_file_name.txt')
        copy_to_bucket("new-files-uploads-data", "new-test-logs", first_file_name)

        # versioning check
        bkt_versioning = s3_resource.BucketVersioning("new-files-uploads-data")
        print(bkt_versioning.status)
        # if bkt_versioning.status == "Suspended":
        #     bkt_versioning.enable()
        print(f"Now Versioning is: {bkt_versioning.status}")

        # delete all objects
        delete_all_objects("new-files-uploads-data")
        delete_all_objects("new-test-logs")
        return "success", 200
    except Exception as e:
        print(e)
        return "Exception in s3 upload", 500


@app.route("/sign_up", methods=["POST"])
def sign_up():
    try:
        all_data = request.json
        username = all_data['username']
        password = all_data['password']
        if "email" in all_data:
            email = all_data['email']
            user_attr = []
            if email:
                user_attr.append(
                    {
                        'Name': 'email',
                        'Value': email
                    }
                )
        else:
            raise ValueError("email is required")
        response = client.sign_up(
            ClientId=os.getenv('CLIENT_ID'),
            Username=username,
            Password=password,
            UserAttributes=user_attr
        )
        return response
    except ValueError:
        raise
    except client.exceptions.UsernameExistsException as e:
        return "User Already Exists", 500
    except Exception as e:
        raise


@app.route("/confirm_sign_up", methods=["POST"])
def confirm_sign_up():
    try:
        all_data = request.json
        username = all_data['username']
        confirmation_code = all_data['confirmation_code']
        response = client.confirm_sign_up(
            ClientId=os.getenv('CLIENT_ID'),
            Username=username,
            ConfirmationCode=confirmation_code,
            ForceAliasCreation=False
        )
        return response
    except client.exceptions.ExpiredCodeException as e:
        return "Confirmation Code is Expired", 500
    except Exception as e:
        return e, 500


@app.route("/login", methods=["POST"])
def login():
    try:
        all_data = request.json
        username = all_data['username']
        password = all_data['password']
        response = client.initiate_auth(
            ClientId=os.getenv('CLIENT_ID'),
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        access_token = response['AuthenticationResult']['AccessToken']
        # validate user
        valid_user = validate_user(access_token)
        user_attr = valid_user['UserAttributes']
        for key in user_attr:
            if key['Name'] == 'email':
                email = key['Value']
        my_data_table.put_item(Item={
            'userId': username,
            'first_name': 'John2',
            'last_name': 'Doe',
            'email': email,
            'created': str(time.time())
        })
        return valid_user
    except client.exceptions.NotAuthorizedException as e:
        return "unauthorized user", 500
    except Exception as e:
        raise


@app.route('/rest-auth', methods=["GET"])
@auth.login_required
def get_response():
    global exporting_threads

    thread_id = random.randint(0, 10000)
    exporting_threads[thread_id] = ExportingThread()
    exporting_threads[thread_id].start()

    return jsonify({'task_id': thread_id})
    return jsonify('You are authorized to see this message')


@app.route('/progress/<int:thread_id>')
def progress(thread_id):
    global exporting_threads

    return jsonify({'progress': exporting_threads[thread_id].progress, 'output': exporting_threads[thread_id].output})


@auth.verify_password
def authenticate(username, password):
    if username and password:
        if username == 'romil' and password == '12345':
            return True
    else:
        return False
    return False


@app.route("/todo", methods=["GET", "POST"])
def todo():
    if request.method == 'GET':
        dic = [{"id": 1, "name": "romil"}, {"id":2, "name": "Chinku"}, 
            {"id": 4, "name":"kaanha"}
        ]
        return jsonify(dic)
    elif request.method == 'POST':
        data = request.get_json()            
        try:
            email = data['email']
            name = data['name']
            _id = todos.insert_one({'email': email, 'name': name}).inserted_id
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if(re.fullmatch(regex, data['email'])):
                return json.dumps(_id, default=str)
                return jsonify({"id":_id}), 200
            else:
                raise EmailNotValidError        
        except EmailNotValidError:
            return jsonify("email not valid"), 500
        except Exception as e:
            print(e)
            return jsonify("error")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000', use_reloader=True)
