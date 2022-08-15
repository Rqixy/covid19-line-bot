from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, UnfollowEvent, MessageEvent, TextMessage,
    TextSendMessage, QuickReply, QuickReplyButton
)
from linebot.models.actions import PostbackAction

from db.user.insert import insert_user_id
from db.user.delete import delete_user_id
from db.infection.print_day import print_infected_day
from db.infection.print_week import print_infected_week
from messages.quick_messages import quick_reply_for_reply

import os

# 1日分のコロナ感染者情報の送信の処理
def infected_info_reply(event: any, day: int):
    infected_info = print_infected_day(day)
    # もし1週間の範囲外の数値が与えられたら範囲外のメッセージを送信する
    if type(infected_info) is str:
        quick_reply_for_reply(event.reply_token, text=infected_info)
        return
    line_text_new_data = infected_info[0] + "\n" + infected_info[1] + "\n" + infected_info[2] + "\n" + infected_info[3] + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
    quick_reply_for_reply(event.reply_token, text=line_text_new_data)

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

# 友達追加したときの処理とメッセージにボタン追加する処理をする
@handler.add(FollowEvent)
def handle_follow(event):
    # ユーザーIDを取得する
    user_id = event.source.user_id
    # データベースにuser_idを格納する
    insert_user_id(user_id)
    # quick replyを表示する
    quick_reply_for_reply(event.reply_token, text="友だち追加ありがとうございます\n\n午後1時に最新のコロナ感染人数を送信するよ！\n\n最新のコロナ感染情報を知りたい場合は、\"最新\"\n1週間のコロナ感染情報を知りたい場合は、\"1周間\"\nと入力してください！\n\nまた下のメッセージボタンからでも確認できるよ！\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n")

# Lineのメッセージの取得と返信内容の設定
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    # 最新の情報を送信する
    if text == '最新' or text == '最新情報':
        day = 0
        infected_info_reply(event=event, day=day)
    # 一日前の情報を送信する
    elif text == '昨日' or text == '1日前' or text == '一日前' or text == 'yesterday':
        day = 1
        infected_info_reply(event=event, day=day)
    elif text == '一昨日' or text == '2日前' or text == '二日前':
        day = 2
        infected_info_reply(event=event, day=day)
    elif text == '3日前' or text == '三日前':
        day = 3
        infected_info_reply(event=event, day=day)
    elif text == '1週間' or text == '１週間' or text == '一週間' or text == 'week':
        week_data_array = print_infected_week()
        line_text_week_data = week_data_array[0] + week_data_array[1] + week_data_array[2] + week_data_array[3] + week_data_array[4] + week_data_array[5] + week_data_array[6] + "\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
        quick_reply_for_reply(event.reply_token, text=line_text_week_data)
    else:
        reply_text = "入力する言葉が違うよ！\n\n最新情報は\"最新\"\n一週間の情報は\"一週間\"\n\nと入力してね！\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
        quick_reply_for_reply(event.reply_token, reply_text)

# ブロックしたらデータベースからuser_idを削除する
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    # ユーザーIDを取得する
    user_id = event.source.user_id
    # データベースから取得したuser_idと一致するuser_idを削除する
    delete_user_id(user_id)

# ポートの設定
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)