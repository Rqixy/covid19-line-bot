from messages.quick_reply import quick_reply_for_send

def send_message_test(text):
    # 登録されているuser_idの人達に最新情報を送信する
    USER_ID = "U6db81b1f3a83373e0ee315628b191fb5"
    quick_reply_for_send(USER_ID, text)