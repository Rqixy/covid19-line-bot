from cProfile import label
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    TextSendMessage, PostbackEvent, ButtonsTemplate,
    QuickReply, QuickReplyButton, URIAction,

)
from linebot.models.actions import PostbackAction
import os
import db

# データベースから最新のデータ情報を持ってくる
new_data_array = db.print_new_data()
line_text_new_data = new_data_array[0] + "\n" + new_data_array[1] + "\n" + new_data_array[2] + "\n" + new_data_array[3] + "\n"
# print(line_text_new_data)

week_data_array = db.print_week_data()
line_text_week_data = week_data_array[0] + "\n" + week_data_array[1] + "\n" + week_data_array[2] + "\n" + week_data_array[3] + "\n" + week_data_array[4] + "\n" + week_data_array[5] + "\n" + week_data_array[6] + "\n"


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
    # quick replyを表示する
    make_quick_reply(event.reply_token, text="友だち追加ありがとうございます\n\n毎朝7時に最新のコロナ感染人数を送信するよ！\n\n最新のコロナ感染情報を知りたい場合は、\"最新\"\n1週間のコロナ感染情報を知りたい場合は、\"1周間\"\nと入力してください！\n\nまた下のメッセージボタンからでも確認できるよ！\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n")

def make_quick_reply(token, text):
    items = []
    items.append(QuickReplyButton(action=PostbackAction(label='最新情報', data='最新情報', text='最新情報')))
    items.append(QuickReplyButton(action=PostbackAction(label='1週間', data='1週間', text='1週間')))
    messages = TextSendMessage(text=text, quick_reply=QuickReply(items=items))
    line_bot_api.reply_message(token, messages=messages)

# Lineのメッセージの取得と返信内容の設定
# LINEでMessageEventが起こった場合に、def以下の関数を実行する
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample',
            text='Hello, my buttons',
            actions=[
                MessageAction(label='Translate Rice', text='米'),
                URIAction(label='Go to line.me', uri='https://line.me'),
            ]
        )
        template_message = TemplateSendMessage(alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == '最新' or text == '最新情報':
        buttons_template = ButtonsTemplate(
            title='コロナ感染最新情報',
            text=line_text_new_data,
            actions=[
                MessageAction(label='最新情報', text='最新情報'),
                MessageAction(label='1週間', text='1週間'),
                URIAction(label='詳しい感染状況はこちらから', uri='https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html'),
            ]
        )
        template_message = TemplateSendMessage(alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        
    elif text == '1週間' or text == '１週間' or text == '一週間' or text == 'week':
        buttons_template = ButtonsTemplate(
            title='1週間のコロナ感染最新情報',
            text=line_text_week_data,
            actions=[
                MessageAction(label='最新情報', text='最新情報'),
                MessageAction(label='1週間', text='1週間'),
                URIAction(label='詳しい感染状況はこちらから', uri='https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html'),
            ]
        )
        template_message = TemplateSendMessage(alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        

    else:
        buttons_template = ButtonsTemplate(
            title='入力が間違っています！',
            text="入力する言葉が違うよ！\n\n最新情報は\"最新\"\n一週間の情報は\"一週間\"\n\nと入力してね！\n",
            actions=[
                MessageAction(label='最新情報', text='最新情報'),
                MessageAction(label='1週間', text='1週間'),
                URIAction(label='詳しい感染状況はこちらから', uri='https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html'),
            ]
        )
        template_message = TemplateSendMessage(alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

# ポートの設定
if __name__ == '__main__':
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)