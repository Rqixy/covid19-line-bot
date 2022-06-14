# 午後1時に自動送信するプログラム
from linebot import LineBotApi
import os
import processing.db as db
import sys
import processing.message as message

# データベースから最新のデータ情報を持ってくる
new_data = db.insert_infected_data()

# もし新しいデータが更新されていなかったらdbのinsert_infected_peopleのtext結果を代入する
if type(new_data) is str:
    # Lineに送る送信メッセージの作成
    line_text_new_data = new_data + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
    print(line_text_new_data)
# もし新しいデータが更新されていなかったらdbのinsert_infected_peopleの配列結果を代入する
elif type(new_data) is list:
    # Lineに送る送信メッセージの作成
    line_text_new_data = new_data[0] + "\n" + new_data[1] + "\n" + new_data[2] + "\n" + new_data[3] + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
    print(line_text_new_data)
else:
    print("ERROR : 情報が何か変です！" + new_data)
    sys.exit()

# アクセストークンの取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

# データベースから登録されているuser_idを全て取得
users_id = db.print_user_id()
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# 登録されているuser_idの人達に最新情報を送信する
for user_id in users_id:
    USER_ID = user_id
    message.make_quick_message(user_id=USER_ID, text=line_text_new_data, line_bot_api=line_bot_api)