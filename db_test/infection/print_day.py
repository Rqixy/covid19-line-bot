import db_test.config as config
import psycopg2

# 引数で与えられたレコードを返す
def print_infected_day(day: int):
    # もし送られてきた数字が１週間の範囲外ならエラー
    if day < 0 or day >= 7:
        text = "入力された値が範囲外だよ！"
        return text

    # データベースに接続する
    with psycopg2.connect(config.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM test_table ORDER BY id DESC LIMIT 1 OFFSET %s;"
            curs.execute(sql, (str(day),))

            new_data = []
            for infected_data in curs.fetchall():
                new_data = [infected_data[4], "    新規感染者数：" + str(infected_data[1]) + "人", "    重症者数(累計)：" + str(infected_data[2]) + "人", "    死亡者数(累計)：" + str(infected_data[3]) + "人"]
            return new_data