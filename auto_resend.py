# 午後1時に新しい情報がなかった際に、午後6時に再送信するプログラム
import sys

from db.infection.insert import insert_infected_info
from messages.send_to_users import send_to_users
from messages.text_on_line import infected_info_on_line

# データベースから最新のデータ情報を持ってくる
new_infected_info = insert_infected_info()

# もうすでに新しいデータが更新されていたら動作を止める
if type(new_infected_info) is str:
    sys.exit()

# もし新しいデータが更新されていなかったら、ユーザーに送信するメッセージを作成する
if type(new_infected_info) is list:
    # ユーザーに送信するメッセージの作成
    line_text_new_info = infected_info_on_line(new_infected_info)
else:
    print("ERROR : 情報が何か変です！" + new_infected_info)
    sys.exit()

# ユーザーに送信する
send_to_users(line_text_new_info)
