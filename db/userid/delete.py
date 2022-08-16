import env
import psycopg2

# ブロックしたユーザーのidと一致するuser_idを削除する
def delete_user_id(user_id: str):
    # データベースに接続する
    with psycopg2.connect(env.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            # 取ってきたuser_idと一致するuser_idのレコードを削除する
            sql = "DELETE FROM users_id WHERE user_id=%s"
            curs.execute(sql, (user_id,))
