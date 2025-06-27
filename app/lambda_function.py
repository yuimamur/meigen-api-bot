import requests
import json
import os

def lambda_handler(event, context):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    headers = {"Content-type": "application/json"}
    data = {"text": "Hello, World!"}

    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    return {
        "statusCode": response.status_code,
        "body": response.text
    }

