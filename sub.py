from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
LINE_USER_ID = "yuuki_yx"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# line_bot_api = LineBotApi("HuKxHNyBohSsalkUavt2uN/WNAsQ+JBlW48b9c6lDId9DP+Sh0lW3LWB7KbMFJw9dCF1jS7qm+SHEXe37z6i69VSbspKxHOc7WMIkHFYDjNC9uIpwmnMUz6691Ul+34S+fQXe8TTdv+Hkg3Q6AfuQQdB04t89/1O/w1cDnyilFU=")

def main():
    pushText = TextSendMessage(Text="テストメッセージ")
    line_bot_api.push_message(LINE_USER_ID, messages=pushText)

if __name__ == "__main__":
    main()