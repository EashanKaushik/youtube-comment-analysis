import boto3
import os
import environ
import json


def trigger_lambda(url):
    environ.Env.read_env()

    s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
    
    try:
        response = s3_client.get_object(
                Bucket=os.environ["AWS_S3_BUCKET"], Key='comment_data/' + url + '.csv'
            )
        
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print('data_exist')
        # dataframe = pd.read_csv(response.get("Body"))
        else:
            raise Exception()
    except Exception:
        print('Data does not exit')
    
        lambda_client = boto3.client(
                    "lambda",
                    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
                )
        
        lambda_payload = {"url":url}
        
        lambda_client.invoke(FunctionName='youtube-comment-analysis-labda', 
                         InvocationType='Event',
                         Payload=json.dumps(lambda_payload).encode('utf-8'))