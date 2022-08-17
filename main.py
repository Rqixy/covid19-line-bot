import os

from flask import Flask, abort, request
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (FollowEvent, MessageEvent, TextMessage,
                            UnfollowEvent)

import env
from db.userid.delete import delete_user_id
from db.userid.insert import insert_user_id
from messages.infected_info_message import (oneday_infected_info_message,
                                            oneweek_infected_info_message)
from messages.messages import reply_message

app = Flask(__name__)

# 環境変数取得
handler = WebhookHandler(env.LINE_CHANNEL_SECRET)

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

    # 返信する
    reply_message(event.reply_token, text="友だち追加ありがとうございます\n\n午後1時に最新のコロナ感染人数を送信するよ！\n\n最新のコロナ感染情報を知りたい場合は、\"最新\"\n1週間のコロナ感染情報を知りたい場合は、\"1周間\"\nと入力してください！\n\nまた下のメッセージボタンからでも確認できるよ！\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n")

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
    # ユーザーからのメッセージを取得する
    event_text = event.message.text

    # ユーザーからのメッセージに対して返信内容を変更する
    if event_text == '今日' or event_text == '最新' or event_text == '最新情報':
        oneday_infected_info_message(event, 0)
    elif event_text == '昨日' or event_text == '1日前' or event_text == '１日前' or event_text == '一日前':
        oneday_infected_info_message(event, 1)
    elif event_text == '一昨日' or event_text == '2日前' or event_text == '２日前' or event_text == '二日前':
        oneday_infected_info_message(event, 2)
    elif event_text == '3日前' or event_text == '３日前' or event_text == '三日前':
        oneday_infected_info_message(event, 3)
    elif event_text == '1週間' or event_text == '１週間' or event_text == '一週間':
        oneweek_infected_info_message(event)
    else:
        error_text = "入力する言葉が違うよ！\n\n最新情報は\"最新\"\n一週間の情報は\"一週間\"\n\nと入力してね！\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
        reply_message(event.reply_token, text=error_text)

# ポートの設定
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
