from cgitb import text
from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton
from linebot.models.actions import PostbackAction
import os
import db


# 新しいデータをスクレイピングして取ってくる
db.insert_infected_data()
# データベースから最新のデータ情報を持ってくる
new_data_array = db.print_new_infected_data()
line_text_new_data = new_data_array[0] + "\n" + new_data_array[1] + "\n" + new_data_array[2] + "\n" + new_data_array[3] + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"

# クイックリプライ
def make_quick_reply(user_id, text):
    items = []
    items.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
    items.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
    messages = TextSendMessage(text=text, quick_reply=QuickReply(items=items))
    line_bot_api.push_message(user_id, messages=messages)


LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

# LINE_CHANNEL_ACCESS_TOKEN = 'HuKxHNyBohSsalkUavt2uN/WNAsQ+JBlW48b9c6lDId9DP+Sh0lW3LWB7KbMFJw9dCF1jS7qm+SHEXe37z6i69VSbspKxHOc7WMIkHFYDjNC9uIpwmnMUz6691Ul+34S+fQXe8TTdv+Hkg3Q6AfuQQdB04t89/1O/w1cDnyilFU='

users_id = db.print_user_id()
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
for user_id in users_id:
    USER_ID = user_id
    make_quick_reply(USER_ID, text=line_text_new_data)