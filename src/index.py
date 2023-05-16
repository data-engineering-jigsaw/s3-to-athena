import json
import boto3
import requests
import io

s3 = boto3.client('s3')

def find_receipts(name):
    url = "https://data.texas.gov/resource/naix-2893.json"
    response = requests.get(url, params = {'taxpayer_name': name})
    return response.json()

def cleaned_name(rest_name):
    cleaned_name = rest_name.lower().replace(' ', '_')
    return cleaned_name

def build_in_mem_file(receipts):
    file = io.StringIO("")
    for receipt in receipts:
        file.write(json.dumps(receipt))
        file.write('\n')
    text = file.getvalue()
    return text

def upload(text, bucket, file_name):
    s3.put_object(
        Body=text,
        Bucket=bucket,
        Key=file_name
    )

