import json
import db_config
import utils


def lambda_handler(event, context):

    print(event)
    
    bucketname = event["Records"][0]["s3"]["bucket"]["name"]
    print(f"bucket name : {bucketname}")

    filepath = event["Records"][0]["s3"]["object"]["key"]
    filename = filepath.split('/')[-1]
    print(f"file name :  {filename}")

    region = vent["Records"][0]["awsRegion"]

    db_name = db_config.db_name
    db_user = db_config.db_user
    db_host = db_config.db_host
    db_password = db_config.db_password
    db_port = db_config.db_port

    print(f"db_name :  {db_name}")
    print(f"db_user :  {db_user}")
    print(f"db_host :  {db_host}")
    print(f"db_password :  {db_pass}")
    print(f"db_port :  {db_port}")

    return {
        'statusCode': 200,
        body: json.dumps('Lambda is success')
    }