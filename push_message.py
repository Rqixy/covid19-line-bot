# 午後1時に自動送信するプログラム

from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton
from linebot.models.actions import PostbackAction
import os
import db


# データベースから最新のデータ情報を持ってくる
new_data = db.insert_infected_data()

# もし新しいデータが更新されていなかったらdbのinsert_infected_peopleのtext結果を代入する
if type(new_data) is str:
    # Lineに送る送信メッセージの作成
    line_text_new_data = new_data + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
    print(line_text_new_data)
# もし新しいデータが更新されていなかったらdbのinsert_infected_peopleの配列結果を代入する
else:
    # Lineに送る送信メッセージの作成
    line_text_new_data = new_data[0] + "\n" + new_data[1] + "\n" + new_data[2] + "\n" + new_data[3] + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
    print(line_text_new_data)

# クイックリプライ
def make_quick_reply(user_id, text):
    items = []
    items.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
    items.append(QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')))
    items.append(QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')))
    items.append(QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')))
    items.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
    messages = TextSendMessage(text=text, quick_reply=QuickReply(items=items))
    line_bot_api.push_message(user_id, messages=messages)

# アクセストークンの取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

# データベースから登録されているuser_idを全て取得
users_id = db.print_user_id()
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# 登録されているuser_idの人達に最新情報を送信する
for user_id in users_id:
    USER_ID = user_id
    make_quick_reply(USER_ID, text=line_text_new_data)