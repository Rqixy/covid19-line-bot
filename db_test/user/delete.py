import db_test.config as config
import psycopg2

# ブロックしたユーザーのidと一致するuser_idを削除する
def delete_user_data(user_id: str):
    # データベースに接続する
    with psycopg2.connect(config.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            # 取ってきたuser_idと一致するuser_idのレコードを削除する
            sql = "DELETE FROM users_id WHERE user_id=%s"
            curs.execute(sql, (user_id,))
