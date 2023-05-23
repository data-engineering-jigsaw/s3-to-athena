import logging.config
import time
from typing import Dict

import boto3
import pandas as pd

DB_NAME = "another-db"
S3_STAGING_DIR = "s3://jigsawtexasresults/output/"
S3_BUCKET_NAME = "jigsawtexasresults"
S3_OUTPUT_DIRECTORY = "output"
AWS_REGION = "us-east-1"

s3_client = boto3.client("s3")
athena_client = boto3.client("athena")


def query_athena():
    response = athena_client.start_query_execution(
        QueryString="SELECT * FROM jigsaw_taylor_sample limit 3",
        QueryExecutionContext={"Database": DB_NAME},
        ResultConfiguration={
            "OutputLocation": S3_STAGING_DIR,
            "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
        },
    )
    return response

def download_query_results(query_response):
    while True:
        try:
            athena_client.get_query_results(QueryExecutionId=query_response["QueryExecutionId"])
            break
        except Exception as err:
            if "not yet finished" in str(err):
                time.sleep(0.01)
            else:
                raise err
    
    local_file = "results.csv"
    s3_client.download_file(
        S3_BUCKET_NAME,
        f"{S3_OUTPUT_DIRECTORY}/{query_response['QueryExecutionId']}.csv",
        local_file)
    return pd.read_csv(local_file)


response = query_athena()
df_data = download_query_results(response)
