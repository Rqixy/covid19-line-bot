# 午後6時に再送信するプログラム
from db.infection.insert import insert_infected_info
from messages.send_message import send_message
import sys

# データベースから最新のデータ情報を持ってくる
new_data = insert_infected_info()

# もうすでに新しいデータが更新されていたら動作を止める
if type(new_data) is str:
    sys.exit()
# もし新しいデータが更新されていなかったらdbのinsert_infected_peopleの配列結果を代入する
elif type(new_data) is list:
    # Lineに送る送信メッセージの作成
    line_text_new_data = new_data[0] + "\n" + new_data[1] + "\n" + new_data[2] + "\n" + new_data[3] + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
else:
    print("ERROR : 情報が何か変です！" + new_data)
    sys.exit()

send_message(line_text_new_data)