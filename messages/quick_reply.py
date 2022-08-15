# クイックメッセージを利用するためのモジュール
from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton
from linebot.models.actions import PostbackAction
import os

# アクセストークンの取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# クイックメッセージボタンの配列
# quick_reply_button = [
#     QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')),
#     QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')),
#     QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')),
#     QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')),
#     QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')),
# ]

# 返信用のクイックリプライの処理
def quick_reply_for_reply(text, token):
    try:
        quick_reply_button = [
            QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')),
            QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')),
            QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')),
            QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')),
            QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')),
        ]

        # quick_reply_button = []
        # quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
        # quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')))
        # quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')))
        # quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')))
        # quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
        messages = TextSendMessage(text, QuickReply(quick_reply_button))
        return line_bot_api.reply_message(token, messages)
    except Exception as e:
        print("メッセージエラー発生！ : " + str(type(e)) + " : " + e.args + " : " + e.message)

# 自動送信用のクイックメッセージの処理
def quick_reply_for_send(text, user_id):
    try:
        quick_reply_button = []
        quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
        quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')))
        quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')))
        quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')))
        quick_reply_button.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
        messages = TextSendMessage(text, QuickReply(quick_reply_button))
        return line_bot_api.push_message(user_id, messages)
    except Exception as e:
        print("メッセージエラー発生！ : " + str(type(e)) + " : " + e.args + " : " + e.message)