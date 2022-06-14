# # テストプログラム
# from linebot import LineBotApi
# import db
# import sys
# import message


# # データベースから最新のデータ情報を持ってくる
# new_data = db.insert_infected_data()

# # もうすでに新しいデータが更新されていたら動作を止める
# if type(new_data) is str:
#     sys.exit()
# # もし新しいデータが更新されていなかったらdbのinsert_infected_peopleの配列結果を代入する
# elif type(new_data) is list:
#     # Lineに送る送信メッセージの作成
#     line_text_new_data = new_data[0] + "\n" + new_data[1] + "\n" + new_data[2] + "\n" + new_data[3] + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
#     print(line_text_new_data)

# # テスト用、user_idを入れる
# # XXX 終わったら必ず削除！！
# user_id = ""

# # アクセストークンの取得
# # XXX 終わったら必ず削除！！
# LINE_CHANNEL_ACCESS_TOKEN = ""
# line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# # 登録されているuser_idの人達に最新情報を送信する
# USER_ID = user_id
# message.make_quick_message(user_id=USER_ID, text=line_text_new_data, line_bot_api=line_bot_api)

def aa(a, b):
    try:
        print(a/b)
    except Exception as e:
        print(e)
        return 'error'

print(aa('a', 'b'))