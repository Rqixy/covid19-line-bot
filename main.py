from flask import Flask, request, abort
from linebot import WebhookHandler
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, UnfollowEvent, MessageEvent, TextMessage,
)
from db.user.insert import insert_user_id
from db.user.delete import delete_user_id
from db.infection.print_week import print_infected_week
from messages.quick_reply import quick_reply_for_reply
from messages.infected_info_reply import infected_info_reply
import os

app = Flask(__name__)

# 環境変数取得
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
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

# 友達追加したときの処理とメッセージにボタン追加する処理をする
@handler.add(FollowEvent)
def handle_follow(event):
    # ユーザーIDを取得する
    user_id = event.source.user_id

    # データベースにuser_idを格納する
    insert_user_id(user_id)

    # quick replyを表示する
    quick_reply_for_reply(event.reply_token, text="友だち追加ありがとうございます\n\n午後1時に最新のコロナ感染人数を送信するよ！\n\n最新のコロナ感染情報を知りたい場合は、\"最新\"\n1週間のコロナ感染情報を知りたい場合は、\"1周間\"\nと入力してください！\n\nまた下のメッセージボタンからでも確認できるよ！\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n")

# ブロックしたらデータベースからuser_idを削除する
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    # ユーザーIDを取得する
    user_id = event.source.user_id
    # データベースから取得したuser_idと一致するuser_idを削除する
    delete_user_id(user_id)

# Lineのメッセージの取得と返信内容の設定
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    event_text = event.message.text

    if event_text == '最新' or event_text == '最新情報':
        day = 0
        infected_info_reply(event, day)
    elif event_text == '昨日' or event_text == '1日前' or event_text == '一日前':
        day = 1
        infected_info_reply(event, day)
    elif event_text == '一昨日' or event_text == '2日前' or event_text == '二日前':
        day = 2
        infected_info_reply(event, day)
    elif event_text == '3日前' or event_text == '三日前':
        day = 3
        infected_info_reply(event, day)
    elif event_text == '1週間' or event_text == '１週間' or event_text == '一週間':
        week_data_array = print_infected_week()
        line_text_week_data = week_data_array[0] + week_data_array[1] + week_data_array[2] + week_data_array[3] + week_data_array[4] + week_data_array[5] + week_data_array[6] + "\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
        quick_reply_for_reply(event.reply_token, text=line_text_week_data)
    else:
        reply_text = "入力する言葉が違うよ！\n\n最新情報は\"最新\"\n一週間の情報は\"一週間\"\n\nと入力してね！\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
        quick_reply_for_reply(event.reply_token, text=reply_text)

# ポートの設定
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)