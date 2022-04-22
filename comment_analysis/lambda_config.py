import boto3
import os
import environ
import json
from io import StringIO

from scrappy.models import Request

import pandas as pd


def trigger_lambda(url, request_id):
    environ.Env.read_env()

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    try:
        response = s3_client.get_object(
            Bucket=os.environ["AWS_S3_BUCKET"], Key="comment_data/" + url + ".csv"
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            Request.objects.get(request_display=request_id).completed = True
        # dataframe = pd.read_csv(response.get("Body"))
        else:
            raise Exception()
    except Exception:

        lambda_client = boto3.client(
            "lambda",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )

        lambda_payload = {"url": url}

        lambda_client.invoke(
            FunctionName="youtube-comment-analysis-labda",
            InvocationType="Event",
            Payload=json.dumps(lambda_payload).encode("utf-8"),
        )


def update_request(request_id):

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    url = Request.objects.get(request_display=request_id).url

    url_request = Request.objects.get(request_display=request_id)

    response = s3_client.get_object(
        Bucket=os.environ["AWS_S3_BUCKET"], Key="comment_data/" + url + ".csv"
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        url_request.completed = True
        url_request.save()
    else:
        raise Exception()


def upload_data(dataset, request_id):
    # Creating Session With Boto3.
    session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    # Creating S3 Resource From the Session.
    s3_res = session.resource("s3")

    csv_buffer = StringIO()

    dataset.to_csv(csv_buffer)

    bucket_name = os.environ["AWS_PUBLIC_BUCKET"]

    s3_object_name = f"{request_id}.csv"

    s3_res.Object(bucket_name, s3_object_name).put(Body=csv_buffer.getvalue())


def check_s3_analyze(request_id):

    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )

        url = Request.objects.get(request_display=request_id).url

        url_request = Request.objects.get(request_display=request_id)

        response = s3_client.get_object(
            Bucket=os.environ["AWS_PUBLIC_BUCKET"], Key=f"{request_id}.csv"
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            return True
        else:
            return False
    except Exception:
        return False


def read_analyzed_data(request_id):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    url = Request.objects.get(request_display=request_id).url

    response = s3_client.get_object(
        Bucket=os.environ["AWS_PUBLIC_BUCKET"], Key=f"{request_id}.csv"
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        dataframe = pd.read_csv(response.get("Body"))
    else:
        raise Exception("No bucket")

    # print(dataframe)
    return dataframe


def read_dataset(request_id):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    url = Request.objects.get(request_display=request_id).url

    response = s3_client.get_object(
        Bucket=os.environ["AWS_S3_BUCKET"], Key="comment_data/" + url + ".csv"
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        dataframe = pd.read_csv(response.get("Body"))
    else:
        raise Exception("No bucket")

    # print(dataframe)
    return dataframe
