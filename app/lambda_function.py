import json
import os
import requests

def lambda_handler(event, context):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    message = {"text": "Hello, world!"}

    response = requests.post(
        webhook_url,
        data=json.dumps(message),
        headers={"Content-Type": "application/json"}
    )

    return {
        "statusCode": response.status_code,
        "body": response.text
    }

