import env
import psycopg2

# 1週間分の感染情報を取得して返す
def oneweek_infected_info() -> list:
    # データベースに接続する
    with psycopg2.connect(env.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM infected_info ORDER BY id;"
            curs.execute(sql)
            week_infected_info_array = []
            for infected_info in curs.fetchall():
                week_infected_info_array.append(infected_info[1] + "\n" + "    新規感染者数：" + str(infected_info[2]) + "人" + "\n" + "    重症者数(累計)：" + str(infected_info[3]) + "人" + "\n" + "    死亡者数(累計)：" + str(infected_info[4]) + "人\n\n")

            return week_infected_info_array