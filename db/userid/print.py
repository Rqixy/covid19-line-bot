import db.config as config
import psycopg2

# user_idを配列で取得して返す
def print_user_id() -> list:
    # データベースに接続する
    with psycopg2.connect(config.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM users_id"
            curs.execute(sql)
            user_id = []
            for row in curs.fetchall():
                user_id.append(row[1])
            return user_id