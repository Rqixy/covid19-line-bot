import string
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton
from linebot.models.actions import PostbackAction


# クイックリプライ
def make_quick_reply(user_id: string, text: string):
    items = []
    items.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
    items.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
    messages = TextSendMessage(text=text, quick_reply=QuickReply(items=items))
    line_bot_api.push_message(user_id, messages=messages)