import requests
import json
import os
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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";

def lambda_handler(event, context):
    res = requests.get("https://api.quotable.io/random")
    data = res.json()
    quote = f"{data['content']} — {data['author']}"

    webhook = os.environ.get(SLACK_WEBHOOK_URL)
    payload = {"text": quote}
    requests.post(webhook, json=payload)

    return {"statusCode": 200, "body": quote}
