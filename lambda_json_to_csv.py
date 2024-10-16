import csv
import json
import boto3

def lambda_handler(event, context):
    
    targetbucket = 'BUCKET NAME'
    csvkey = 'departement.csv'
    jsonkey = 'departement.json'
    
    s3 = boto3.resource('s3')
    csv_object = s3.Object(targetbucket, csvkey)
    csv_content = csv_object.get()['Body'].read().splitlines()
    s3_client = boto3.client('s3')
    l = []
    
    for line in csv_content:
        x = json.dumps(line.decode('utf-8')).split(',')
        dept_id = str(x[0])
        dept_name = str(x[1])
        
        y = '{ "departement_id": ' + dept_id + '"' + ','  \
            + ' "departement_name": ' + '"' + dept_name + '"' + '}'
        l.append(y)

    s3_client.put_object(
    	Bucket=targetbucket,
    	Body= str(l).replace("'",""),
    	Key=jsonkey,
    	ServerSideEncryption='AES256'
    )
