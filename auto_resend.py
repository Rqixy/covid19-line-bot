# 午後1時に新しい情報がなかった際に、午後6時に再送信するプログラム
import sys

from db.infection.insert_infected_info import insert_infected_info
from messages.push_to_users import push_to_users
from messages.text_on_line import infected_info_on_line

# 最新のデータ情報を取得し、データベースに登録する
new_infected_info = insert_infected_info()

# もうすでに新しいデータが更新されていたら動作を止める
if type(new_infected_info) is str:
    sys.exit()

# 新しい情報が取得できていたら、LINEに送信するテキストに変換して送信する
if type(new_infected_info) is list:
    # ユーザーに送信するメッセージの作成
    line_text = infected_info_on_line(new_infected_info)
else:
    print("ERROR : 情報が何か変です！" + new_infected_info)
    sys.exit()

# ユーザーに送信する
push_to_users(line_text)
