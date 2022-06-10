# クイックメッセージを利用するためのモジュール
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton
from linebot.models.actions import PostbackAction

# プッシュ用のクイックメッセージの生成メソッド
def make_quick_message(text, line_bot_api, token=None, user_id=None):
    try:
        items = []
        items.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
        items.append(QuickReplyButton(action=PostbackAction(label='昨日', data='昨日', text='昨日')))
        items.append(QuickReplyButton(action=PostbackAction(label='一昨日', data='一昨日', text='一昨日')))
        items.append(QuickReplyButton(action=PostbackAction(label='3日前', data='3日前', text='3日前')))
        items.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
        messages = TextSendMessage(text=text, quick_reply=QuickReply(items=items))
        # 個人からのメッセージが送られたら
        if token != None and user_id == None:
            return line_bot_api.push_message(token, messages=messages)
        # 自動送信でuser_idを受けっとたら
        elif token == None and user_id != None:
            return line_bot_api.push_message(user_id, messages=messages)
    except Exception as e:
        print("メッセージエラー発生！ : " + e)