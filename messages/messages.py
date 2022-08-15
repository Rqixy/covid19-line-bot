# クイックメッセージを利用するためのモジュール
import os

from linebot import LineBotApi
from linebot.models import QuickReply, QuickReplyButton, TextSendMessage
from linebot.models.actions import PostbackAction

# アクセストークンの取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# クイックリプライボタン作成
quick_reply_buttons = [
    QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')),
    QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')),
    QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')),
    QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')),
    QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間'))
]

# 返信処理
def reply_message(token, text):
    try:
        messages = TextSendMessage(text=text, quick_reply=QuickReply(items=quick_reply_buttons))
        return line_bot_api.reply_message(token, messages=messages)
    except Exception as e:
        print("メッセージエラー発生！ : " + str(type(e)) + " : " + e.args + " : " + e.message) 

# 自動送信用の処理
def push_message(user_id, text):
    try:
        messages = TextSendMessage(text=text, quick_reply=QuickReply(items=quick_reply_buttons))
        return line_bot_api.push_message(user_id, messages=messages)
    except Exception as e:
        print("メッセージエラー発生！ : " + str(type(e)) + " : " + e.args + " : " + e.message)
