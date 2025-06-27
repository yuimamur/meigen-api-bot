# 必要なモジュールをインポート
# requests: HTTPリクエストを送るためのライブラリ
# datetime: 現在の日付を取得する標準ライブラリ
import requests
from datetime import datetime
import os
# 気象庁のAPIから天気情報を取得してDiscord向けに整形する関数
def fetch_weather():
    try:
        # 概況情報と詳細天気情報のAPIエンドポイント（神奈川県を例に）
        overview_url = 'https://www.jma.go.jp/bosai/forecast/data/overview_forecast/140000.json'
        detail_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/140000.json'

        # JSONデータを取得
        overview = requests.get(overview_url).json()
        detail = requests.get(detail_url).json()

        # 地域名（例: 東部）を取得
        area_name = detail[0]['timeSeries'][0]['areas'][0]['area']['name']
        # 今日の日付を YYYY-MM-DD の形式で取得
        date_str = datetime.now().strftime('%Y-%m-%d')
        # 今日の天気（例: 晴れ時々曇り）を取得
        weather_today = detail[0]['timeSeries'][0]['areas'][0]['weathers'][0]

        # 降水確率を取得し、時間帯ごとに表示用の文字列に整形
        pops_series = detail[0]['timeSeries'][1]
        pop_times = pops_series['timeDefines']
        pops = pops_series['areas'][0]['pops']
        pop_text = "☔ 降水確率：\n"
        for time, pop in zip(pop_times, pops):
            hour_str = time[11:16]  # 例: '06:00'
            pop_value = pop if pop else "---"
            pop_text += f"・{hour_str} 時 ～ : {pop_value}%\n"

        # 概況テキスト（文章による天気の説明）を取得
        overview_text = overview["text"]

        # 通知メッセージ全体を組み立てる
        message = (
            f"📅 {date_str} の天気情報（{area_name}）\n"
            f"🌤 今日の天気: {weather_today}\n"
            f"{pop_text.strip()}\n"
            f"📝 概況:\n{overview_text}"
        )
        return message

    except Exception as e:
        # 例外が発生した場合はエラーメッセージを返す
        return f"[エラー] 天気情報の取得に失敗しました: {str(e)}"

# DiscordのWebhookにPOSTしてメッセージを通知する関数
def send_to_discord(message, webhook_url):
    try:
        data = {"content": message}
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            raise Exception(f"Discord通知失敗: {response.status_code}")
    except Exception as e:
        print(f"[エラー] Discord送信に失敗: {str(e)}")

# AWS Lambdaのエントリーポイント関数
def lambda_handler(event, context):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    weather_message = fetch_weather()
    send_to_discord(weather_message, webhook_url)
    return {
        'statusCode': 200,
        'body': '天気通知完了'
    }
