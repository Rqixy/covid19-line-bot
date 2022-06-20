import db_config as db
import psycopg2
from datetime import datetime, timezone, timedelta

db_url = db.DATABASE_URL

# user_idを取ってきてテーブルに格納する
def insert_user_data(user_id: str):
    # データベースに接続する
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as curs:
            #ユーザーが登録した日付の取得
            JST = timezone(timedelta(hours=+9))
            now = datetime.now(JST).isoformat()
            # user_idをデータベースに登録する
            sql = "INSERT INTO users_id (user_id, created_at) VALUES (%s, %s)"
            curs.execute(sql, (user_id, now))

# ブロックしたユーザーのidと一致するuser_idを削除する
def delete_user_data(user_id: str):
    # データベースに接続する
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as curs:
            # 取ってきたuser_idと一致するuser_idのレコードを削除する
            sql = "DELETE FROM users_id WHERE user_id=%s"
            curs.execute(sql, (user_id,))

# user_idを配列で取得して返す
def print_user_id():
    # データベースに接続する
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM users_id"
            curs.execute(sql)
            user_id = []
            for row in curs.fetchall():
                user_id.append(row[1])
            return user_id