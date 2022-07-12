import boto3


bucket_name = 'new-files-uploads-data'
s3_client = boto3.client('s3',aws_access_key_id="AKIA2QCI4BBXNZYBOTJ7",
         aws_secret_access_key="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")

versions = s3_client.list_object_versions(Bucket=bucket_name)
# print(versions['Versions'])

for version in versions['Versions']:
    version_id = version['VersionId']
    file_key = version['Key']

    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=file_key,
        VersionId=version_id,
    )
    data = response['Body'].read()
    print(data)