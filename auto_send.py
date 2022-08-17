# 午後1時に自動送信するプログラム
import sys

from db.infection.insert_infected_info import insert_infected_info
from messages.push_to_users import push_to_users
from messages.text_on_line import infected_info_on_line

# 最新のデータ情報を取得し、データベースに登録する
new_infected_info = insert_infected_info()

# 送られてきた情報が文字列型なら、更新されていないか何かしらのエラーが発生したので、そのメッセージを送信する
if type(new_infected_info) is str:
    line_text = new_infected_info + "\n\n詳しい感染状況はこちらのサイトから確認してね！\nhttps://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html\n"

# 新しい情報が取得できていたら、LINEに送信するテキストに変換して送信する
if type(new_infected_info) is list:
    line_text = infected_info_on_line(new_infected_info)
else:
    print("ERROR : 情報が何か変です！" + new_infected_info)
    sys.exit()

# ユーザーに送信する
push_to_users(line_text)
