import requests
import os
from datetime import datetime

# 気象庁のAPIから天気情報を取得してDiscord向けに整形する関数
def fetch_weather():
    try:
        overview_url = 'https://www.jma.go.jp/bosai/forecast/data/overview_forecast/140000.json'
        detail_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/140000.json'

        overview = requests.get(overview_url, timeout=5).json()
        detail = requests.get(detail_url, timeout=5).json()

        area_name = detail[0]['timeSeries'][0]['areas'][0]['area']['name']
        date_str = datetime.now().strftime('%Y-%m-%d')
        weather_today = detail[0]['timeSeries'][0]['areas'][0]['weathers'][0]

        pops_series = detail[0]['timeSeries'][1]
        pop_times = pops_series['timeDefines']
        pops = pops_series['areas'][0]['pops']
        pop_text = "☔ 降水：\n"
        for time, pop in zip(pop_times, pops):
            hour_str = time[11:16]
            pop_value = pop if pop else "---"
            pop_text += f"・{hour_str} 時 ～ : {pop_value}%\n"

        overview_text = overview["text"]

        message = (
            f"📅 {date_str} の天気情報（{area_name}）\n"
            f"🌤 今日の天気: {weather_today}\n"
            f"{pop_text.strip()}\n"
            f"📝 状況:\n{overview_text}\n"
        )
        return message

    except Exception as e:
        return f"[エラー] 天気情報の取得失敗しました: {str(e)}"

# Discordにメッセージを送信する関数
def send_to_discord(message, webhook_url):
    try:
        data = {"content": message}
        response = requests.post(webhook_url, json=data, timeout=5)
        if response.status_code != 204:
            raise Exception(f"Discord通知失敗: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[エラー] Discord送信に失敗: {str(e)}")

# Lambdaのエントリポイント
def lambda_handler(event, context):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return {
            'statusCode': 500,
            'body': '[エラー] Webhook URLが設定されていません'
        }

    weather_message = fetch_weather()
    send_to_discord(weather_message, webhook_url)
    return {
        'statusCode': 200,
        'body': '天気通知完了'
    }

