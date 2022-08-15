# 午後1時に自動送信するプログラム
import sys

from db.infection.insert import insert_infected_info
from messages.send_to_users import send_to_users
from messages.text_on_line import infected_info_on_line

# データベースから最新のデータ情報を持ってくる
new_infected_info = insert_infected_info()

# もし新しいデータが更新されていなかったらdbのinsert_infected_peopleのtext結果を代入する
if type(new_infected_info) is str:
    # Lineに送る送信メッセージの作成
    line_text_new_infected_info = new_infected_info + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"
# もし新しいデータが更新されていなかったらdbのinsert_infected_peopleの配列結果を代入する
elif type(new_infected_info) is list:
    # Lineに送る送信メッセージの作成
    line_text_new_info = infected_info_on_line(new_infected_info)
else:
    print("ERROR : 情報が何か変です！" + new_infected_info)
    sys.exit()

# ユーザーに送信する
send_to_users(line_text_new_info)
