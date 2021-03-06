import string
import processing.scraping as scraping
import psycopg2
from datetime import datetime, timezone, timedelta
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

# 一番古いレコードを削除するためのid取得をして返す
def first_data_id():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM infected_people ORDER BY id LIMIT 1;"
            curs.execute(sql)
            records = curs.fetchall()
            first_data_id = ""
            for row in records:
                first_data_id = str(row[0])
            return first_data_id

# 感染者データの追加
def insert_infected_data():
    # スクレイピングを行い、配列で取得する
    infected_people_array = scraping.infected_people_scraping()

    # スクレイピングで情報が取得できていなかったら情報を取得できなかったことを送信する
    if infected_people_array == None:
        text = "情報が正しく取得されませんでした\n午後6時にもう一度送信されます！"
        return text

    # データベースに接続する
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            # もし新しいデータが入ってこなかったら新しいデータが無いことを送信する
            sql = "SELECT * FROM infected_people ORDER BY id DESC LIMIT 1;"
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
            sql = "INSERT INTO infected_people (new_people, severe_people, deaths, infected_day) VALUES (%s, %s, %s, %s)"
            curs.execute(sql, (infected_people_array[1], infected_people_array[2], infected_people_array[3], infected_people_array[0]))

            # レコードが7個より大きくなったら一番古いレコードを削除する
            curs.execute("SELECT * FROM infected_people;")
            records = curs.fetchall()
            counts = len(records)
            if counts > 7:
                curs.execute("DELETE FROM infected_people WHERE id = %s" , (first_data_id(),))

            # 新しいデータが更新されたら最新情報を表示する
            sql = "SELECT * FROM infected_people ORDER BY id DESC LIMIT 1;"
            curs.execute(sql)
            new_data = []
            for row in curs.fetchall():
                new_data = [row[4], "    新規感染者数：" + str(row[1]) + "人", "    重症者数(累計)：" + str(row[2]) + "人", "    死亡者数(累計)：" + str(row[3]) + "人"]
            return new_data

# user_idを取ってきてテーブルに格納する
def insert_user_data(user_id: string):
    # データベースに接続する
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            #ユーザーが登録した日付の取得
            JST = timezone(timedelta(hours=+9))
            now = datetime.now(JST).isoformat()
            # user_idをデータベースに登録する
            sql = "INSERT INTO users_id (user_id, created_at) VALUES (%s, %s)"
            curs.execute(sql, (user_id, now))

# ブロックしたユーザーのidと一致するuser_idを削除する
def delete_user_data(user_id: string):
    # データベースに接続する
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            # 取ってきたuser_idと一致するuser_idのレコードを削除する
            sql = "DELETE FROM users_id WHERE user_id=%s"
            curs.execute(sql, (user_id,))

# 引数で与えられたレコードを返す
def print_infected_data(day: int)-> any:
    # もし送られてきた数字が１週間の範囲外ならエラー
    if day < 0 or day >= 7:
        text = "入力された値が範囲外だよ！"
        return text
    # データベースに接続する
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM infected_people ORDER BY id DESC LIMIT 1 OFFSET %s;"
            curs.execute(sql, (str(day),))
            new_data = []
            for row in curs.fetchall():
                new_data = [row[4], "    新規感染者数：" + str(row[1]) + "人", "    重症者数(累計)：" + str(row[2]) + "人", "    死亡者数(累計)：" + str(row[3]) + "人"]
            return new_data

# 1週間分の感染情報を取得して返す
def print_week_infected_data():
    # データベースに接続する
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM infected_people ORDER BY id;"
            curs.execute(sql)
            week_data = []
            for row in curs.fetchall():
                week_data.append(row[4] + "\n" + "    新規感染者数：" + str(row[1]) + "人" + "\n" + "    重症者数(累計)：" + str(row[2]) + "人" + "\n" + "    死亡者数(累計)：" + str(row[3]) + "人\n\n")
            return week_data

# user_idを配列で取得して返す
def print_user_id():
    # データベースに接続する
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            sql = "SELECT * FROM users_id"
            curs.execute(sql)
            user_id = []
            for row in curs.fetchall():
                user_id.append(row[1])
            return user_id
