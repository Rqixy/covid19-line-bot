from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

# 環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# line_bot_api = LineBotApi("HuKxHNyBohSsalkUavt2uN/WNAsQ+JBlW48b9c6lDId9DP+Sh0lW3LWB7KbMFJw9dCF1jS7qm+SHEXe37z6i69VSbspKxHOc7WMIkHFYDjNC9uIpwmnMUz6691Ul+34S+fQXe8TTdv+Hkg3Q6AfuQQdB04t89/1O/w1cDnyilFU=")
# handler = WebhookHandler("92f0e2cf05b3db08e09a8fc4230fe5c9")

# Webhookからのリクエストをチェックする
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得する
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得する
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合例外を出す。
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    # handleの処理を終えればOK
    return 'OK'


# Lineのメッセージの取得と返信内容の設定

# LINEでMessageEventが起こった場合に、def以下の関数を実行する
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# ポートの設定
if __name__ == '__main__':
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)