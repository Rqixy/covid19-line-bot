from db.userid.print import print_user_id
from messages.messages import push_message

# データベースに登録されているuser_idの人達にメッセージを送信する
def send_to_users(text):
    # データベースから登録されているuser_idを全て取得
    users_id = print_user_id()

    for user_id in users_id:
        push_message(user_id, text)