from db.user.print import print_user_id
from messages.quick_reply import quick_reply_for_send

def send_message(text):
    # データベースから登録されているuser_idを全て取得
    users_id = print_user_id()
    # 登録されているuser_idの人達に最新情報を送信する
    for user_id in users_id:
        USER_ID = user_id
        quick_reply_for_send(USER_ID, text)