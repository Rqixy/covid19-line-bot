import os
import sys
import psycopg2
import db_config_test as db
sys.path.append(os.path.join(os.path.dirname(__file__), '../scraping_test'))
import scraping_test as scraping

db_url = db.DATABASE_URL

# 感染者データの追加
def insert_infected_data():
    # スクレイピングを行い、配列で取得する
    infected_people_array = scraping.infected_people_scraping()

    # スクレイピングで情報が取得できていなかったら情報を取得できなかったことを送信する
    if infected_people_array == None:
        text = "情報が正しく取得されませんでした\n午後6時にもう一度送信されます！"
        return text

    # データベースに接続する
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as curs:
            # もし新しいデータが入ってこなかったら新しいデータが無いことを送信する
            sql = "SELECT * FROM test_table ORDER BY id DESC LIMIT 1;"
            curs.execute(sql)
            records = curs.fetchall()
            result = ""
            for row in records:
                result = str(row[4])

            # スクレイピングで新しく取得した日付と、最後のレコードにある日付を比較して
            # 同じなら更新されていないことを伝える
            if result == infected_people_array[0]:
                text = "新しい感染者情報が更新されていません！\n午後6時にもう一度送信されます！"
                return text

            # スクレイピングで取ってきた配列のデータを格納する
            sql = "INSERT INTO test_table (new_people, severe_people, deaths, infected_day) VALUES (%s, %s, %s, %s)"
            curs.execute(sql, (infected_people_array[1], infected_people_array[2], infected_people_array[3], infected_people_array[0]))

            # レコードが7個より大きくなったら一番古いレコードを削除する
            curs.execute("SELECT * FROM test_table;")
            records = curs.fetchall()
            counts = len(records)
            if counts > 7:
                curs.execute("DELETE FROM test_table WHERE id = %s" , (db.first_data_id(),))

            # 新しいデータが更新されたら最新情報を表示する
            sql = "SELECT * FROM test_table ORDER BY id DESC LIMIT 1;"
            curs.execute(sql)
            new_data = []
            for row in curs.fetchall():
                new_data = [row[4], "    新規感染者数：" + str(row[1]) + "人", "    重症者数(累計)：" + str(row[2]) + "人", "    死亡者数(累計)：" + str(row[3]) + "人"]
            return new_data

# 引数で与えられたレコードを返す
def print_infected_data(day: int)-> any:
    # もし送られてきた数字が１週間の範囲外ならエラー
    if day < 0 or day >= 7:
        text = "入力された値が範囲外だよ！"
        return text
    # データベースに接続する
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM test_table ORDER BY id DESC LIMIT 1 OFFSET %s;"
            curs.execute(sql, (str(day),))
            new_data = []
            for row in curs.fetchall():
                new_data = [row[4], "    新規感染者数：" + str(row[1]) + "人", "    重症者数(累計)：" + str(row[2]) + "人", "    死亡者数(累計)：" + str(row[3]) + "人"]
            return new_data

# 1週間分の感染情報を取得して返す
def print_week_infected_data():
    # データベースに接続する
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM test_table ORDER BY id;"
            curs.execute(sql)
            week_data = []
            for row in curs.fetchall():
                week_data.append(row[4] + "\n" + "    新規感染者数：" + str(row[1]) + "人" + "\n" + "    重症者数(累計)：" + str(row[2]) + "人" + "\n" + "    死亡者数(累計)：" + str(row[3]) + "人\n\n")
            return week_data

print(insert_infected_data())