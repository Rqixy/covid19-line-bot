import db_test.config as config
import psycopg2

# 1週間分の感染情報を取得して返す
def print_week_infected_data():
    # データベースに接続する
    with psycopg2.connect(config.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM test_table ORDER BY id;"
            curs.execute(sql)
            week_data = []
            for row in curs.fetchall():
                week_data.append(row[4] + "\n" + "    新規感染者数：" + str(row[1]) + "人" + "\n" + "    重症者数(累計)：" + str(row[2]) + "人" + "\n" + "    死亡者数(累計)：" + str(row[3]) + "人\n\n")
            
            return week_data