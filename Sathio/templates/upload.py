import boto3
from botocore.exceptions import NoCredentialsError


ACCESS_KEY = 'AKIA2MEORWBCW6D5RPZO'
SECRET_KEY = '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'

session = boto3.Session(
aws_access_key_id=ACCESS_KEY,
aws_secret_access_key=SECRET_KEY,
region_name='ap-south-1')
s3 = session.resource('s3')
response = s3_client.list_objects_v2(Bucket='sathio-production', Prefix='uploads/')
  if response:
      for obj in response['Contents']:
          if mykey == obj['Key']:
              return True
  return False

if key_exists('uploads/', 'sathio-production'):
    print("key exists")
else:
    print("safe to put new bucket object")

# base_path = '/home/jiyoindia-lenovo/django_rest_projects/s3_05092020/uploads'

# import os
# counter = 0
# for file in os.listdir(base_path):
# file_name = base_path+'/'+file
# try:
# s3.upload_file(file_name, 'pro-sathio-bucket', 'media/{}'.format(file))
# counter+=1
# print("Upload Successful",counter)
# except Exception as e:
# print("The file was not found",e)
# except NoCredentialsError:
# print("Credentials not available"