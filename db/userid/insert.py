import env
import psycopg2

# user_idを取ってきてテーブルに格納する
def insert_user_id(user_id: str):
    # データベースに接続する
    with psycopg2.connect(env.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            # user_idをデータベースに登録する
            sql = "INSERT INTO users_id (user_id) VALUES (%s)"
            curs.execute(sql, (user_id,))

