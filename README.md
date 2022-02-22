毎日正午に最新の感染者情報が自動送信されるLineBotです。

チャットから最新情報と一週間の感染情報が確認出来ます。

開発環境はPython,PostgreSQL,Heroku,UptimeRobotを利用しています。

情報は[厚生労働省](https://www.mhlw.go.jp/stf/covid-19/kokunainohasseijoukyou.html "covid-19 kokunainohasseijoukyou")こちらからスクレイピングして取ってきております。
スクレイピングは毎日正午に一度だけ行うようにし、Lineから最新情報を取ってくる時は保存したデータベースから取ってくるようにすることで、負荷を掛けないようにしました。
スクレピングしているので、サイトからの取得が出来なくなったら、サービス終了とします。

Lineの自動送信を行うために登録した際にUserIdを取得されていただいております。
ブロックするとUserIdがデータベースから削除されるようになっておりますのでご安心ください。

```main.py
# こちらがLineBotを友達追加した時のuser_id取得処理です。
@handler.add(FollowEvent)
def handle_follow(event):
    # ユーザーIDを取得する
    user_id = event.source.user_id
    # データベースにuser_idを格納する
    db.insert_user_data(user_id)

# こちらがLineBotをブロックした時のuser_id削除処理です。
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    # ユーザーIDを取得する
    user_id = event.source.user_id
    # データベースから取得したuser_idと一致するuser_idを削除する
    db.delete_user_data(user_id)
```

```db.py
# こちらがデータベースでのuser_id取得した時の処理です。
# user_idを取ってきてテーブルに格納する
def insert_user_data(user_id):
    # データベースに接続する
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            #ユーザーが登録した日付の取得
            JST = timezone(timedelta(hours=+9))
            now = datetime.now(JST).isoformat()
            # user_idをデータベースに登録する
            sql = "INSERT INTO users_id (user_id, created_at) VALUES (%s, %s)"
            curs.execute(sql, (user_id, now))

# こちらがデータベースでのuser_id削除した時の処理です。
# ブロックしたユーザーのidと一致するuser_idを削除する
def delete_user_data(user_id):
    # データベースに接続する
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            # 取ってきたuser_idと一致するuser_idのレコードを削除する
            sql = "DELETE FROM users_id WHERE user_id=%s"
            curs.execute(sql, (user_id,))
```

しかし、個人で作ったものであり、何かあった際に責任取れないので自己責任で登録のほうお願いします。

こちらがLineBotのQRコードになります。良かったら使ってみてください。
![LineBot](https://raw.githubusercontent.com/Rqixy/covid19-line-bot/master/covid19-linebot-QRimage.jpg "Covid-19LineBot")