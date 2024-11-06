# Importing necessary libraries
from datetime import datetime
import pandas as pd
import boto3
from io import StringIO

# Defining handle_insert function
def handle_insert(record):
    print("Handling Insert: ", record)
    data_dict = {}

    for key, value in record['dynamodb']['NewImage'].items():
        for dt, col in value.items():
            data_dict.update({key: col})

    dff = pd.DataFrame([data_dict])
    return dff

# Defining lambda handler
def lambda_handler(event, context):
    print("Event:", event)
    
    # Check if 'Records' exists in the event
    if 'Records' not in event:
        print("No 'Records' key in event")
        return {
            'statusCode': 400,
            'body': "Event does not contain 'Records'."
        }
    
    df = pd.DataFrame()

    # Process each record in the event
    for record in event['Records']:
        table = record['eventSourceARN'].split("/")[1]

        if record['eventName'] == "INSERT": 
            dff = handle_insert(record)
            df = pd.concat([df, dff], ignore_index=True)  # Append to main DataFrame

    if not df.empty:
        all_columns = list(df)
        df[all_columns] = df[all_columns].astype(str)

        # Format the file path
        path = table + "_" + str(datetime.now()) + ".csv"
        
        # Write DataFrame to CSV buffer
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Initialize S3 client and upload CSV
        s3 = boto3.client('s3')
        bucketName = "weatherapi-de-project-landing-bucket"
        key = "snowflake/" + table + "_" + str(datetime.now()) + ".csv"
        print("S3 Key:", key)
        
        s3.put_object(Bucket=bucketName, Key=key, Body=csv_buffer.getvalue())
        print('Successfully uploaded to S3:', key)

    print('Successfully processed %s records.' % str(len(event['Records'])))
    
    return {
        'statusCode': 200,
        'body': "Records processed successfully."
    }
