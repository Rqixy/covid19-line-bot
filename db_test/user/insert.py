import db_test.config as config
import psycopg2

# user_idを取ってきてテーブルに格納する
def insert_user_data(user_id: str):
    # データベースに接続する
    with psycopg2.connect(config.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            # user_idをデータベースに登録する
            sql = "INSERT INTO users_id (user_id) VALUES (%s)"
            curs.execute(sql, (user_id,))

