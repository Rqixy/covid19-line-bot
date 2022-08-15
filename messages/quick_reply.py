# クイックメッセージを利用するためのモジュール
from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton
from linebot.models.actions import PostbackAction
import os

# アクセストークンの取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

items = []
items.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
items.append(QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')))
items.append(QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')))
items.append(QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')))
items.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))

# 送信用のクイックメッセージの処理
def quick_reply_for_send(user_id, text):
    try:
        # items = []
        # items.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
        # items.append(QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')))
        # items.append(QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')))
        # items.append(QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')))
        # items.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
        messages = TextSendMessage(text=text, quick_reply=QuickReply(items=items))

        return line_bot_api.push_message(user_id, messages=messages)
    except Exception as e:
        print("メッセージエラー発生！ : " + str(type(e)) + " : " + e.args + " : " + e.message)

# 返信用のクイックリプライの処理
def quick_reply_for_reply(token, text):
    try:
        # items = []
        # items.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
        # items.append(QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')))
        # items.append(QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')))
        # items.append(QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')))
        # items.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
        messages = TextSendMessage(text=text, quick_reply=QuickReply(items=items))

        return line_bot_api.reply_message(token, messages=messages)
    except Exception as e:
        print("メッセージエラー発生！ : " + str(type(e)) + " : " + e.args + " : " + e.message) 