import requests
import json
import os

def lambda_handler(event, context):
    # 名言を取得
    res = requests.get("https://api.quotable.io/random")
    data = res.json()
    quote = f"{data['content']} — {data['author']}"

    # Webhook URLを環境変数から取得
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    # Slack に送る payload
    payload = {"text": quote}

    # Slack へ送信
    response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

    return {
        "statusCode": response.status_code,
        "body": response.text
    }

