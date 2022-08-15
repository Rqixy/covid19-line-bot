import db.config as config
import psycopg2


# 引数で与えられたレコードを返す
def oneday_infected_info(num: int) -> (list | str):
    # もし送られてきた数字がレコードの範囲外ならエラー
    if num < 0 or num >= 7:
        error_text = "入力された値が範囲外だよ！"
        return error_text

    # データベースに接続する
    with psycopg2.connect(config.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM infected_people ORDER BY id DESC LIMIT 1 OFFSET %s;"
            curs.execute(sql, (str(num),))

            infected_info_array = []
            for infected_info in curs.fetchall():
                infected_info_array = [infected_info[4], "    新規感染者数：" + str(infected_info[1]) + "人", "    重症者数(累計)：" + str(infected_info[2]) + "人", "    死亡者数(累計)：" + str(infected_info[3]) + "人"]

            return infected_info_array
