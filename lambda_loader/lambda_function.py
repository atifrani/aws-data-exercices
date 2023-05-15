import json
import db_config
from utils import map_name_table, make_conn, execute_query, import_csv_from_s3


def lambda_handler(event, context):

    print(event)
    
    bucketname = event["Records"][0]["s3"]["bucket"]["name"]
    print(f"bucket name : {bucketname}")

    filepath = event["Records"][0]["s3"]["object"]["key"]
    filename = filepath.split('/')[-1]
    print(f"file name :  {filename}")

    region = event["Records"][0]["awsRegion"]

    db_name = db_config.db_name
    db_schema = db_config.db_schema
    db_user = db_config.db_user
    db_host = db_config.db_host
    db_password = db_config.db_password
    db_port = db_config.db_port

    print(f"db_name :  {db_name}")
    print(f"db_user :  {db_user}")
    print(f"db_host :  {db_host}")
    print(f"db_password :  {db_password}")
    print(f"db_port :  {db_port}")

    # retrieve rds table name from file name
    target_table = map_name_table(filename)  
    print (f"la table rds: {target_table}")

    # Get connction
    conn = make_conn(db_name, db_user, db_host, db_password, db_port)
    
    # Create aws_s3 extension for RDS postgresql if not exist
    execute_query(conn, "CREATE EXTENSION IF NOT EXISTS aws_s3 CASCADE;")

    # import csv file from s3 to rds
    options = f"(format csv, delimiter '','', HEADER true, ENCODING ''utf-8'')"
    import_csv_from_s3(conn, target_table, db_schema, bucketname, filename, region, options)

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda is success')
    }
