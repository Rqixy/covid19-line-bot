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
import db

# データベースから最新のデータ情報を持ってくる
new_data_array = db.print_new_data()
line_text_new_data = new_data_array[0] + "\n" + new_data_array[1] + "\n" + new_data_array[2] + "\n" + new_data_array[3] + "\n" "詳しくは下記のURLから確認してね！" + "\n\n" + "https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html"
# print(line_text_new_data)

week_data_array = db.print_week_data()
line_text_week_data = week_data_array[0] + "\n" + week_data_array[1] + "\n" + week_data_array[2] + "\n" + week_data_array[3] + "\n" + week_data_array[4] + "\n" + week_data_array[5] + "\n" + week_data_array[6] + "\n\n" + "https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html"

app = Flask(__name__)

# 環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
    text = event.message.text
    if text in ['最新', '最新情報']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=line_text_new_data)
        )
    elif text in ['1週間', '１週間', '一週間', 'week']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=week_data_array)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="入力する言葉が違うよ！\n\n最新情報は\"最新\"\n一週間の情報は\"一週間\"\n\nと入力してね！")
        )

# ポートの設定
if __name__ == '__main__':
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)