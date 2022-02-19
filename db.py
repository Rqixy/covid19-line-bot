import scraping
import sqlite3
from datetime import datetime, timedelta


# 感染者データベース作成
def create_data_db():
    db_name = 'infected_people.db'
    # データベースを作成する
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # データベースにテーブルが存在しなかったら作成する
    sql = """
        CREATE TABLE IF NOT EXISTS infected_people (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            new_people INTEGER NOT NULL,
            severe_people INTEGER NOT NULL,
            deaths INTEGER NOT NULL,
            created_at STRING NOT NULL
        );
    """
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

# ユーザーデータベース作成
def create_user_db():
    db_name = 'user.db'
    # データベースを作成する
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # データベースにテーブルが存在しなかったら作成する
    sql = """
        CREATE TABLE IF NOT EXISTS user.db (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id STRING NOT NULL,
            created_at STRING NOT NULL
        );
    """
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

# データの追加
def insert_data():
    db_name = 'infected_people.db'
    # データベースを作成する
    con = sqlite3.connect(db_name)
    cur = con.cursor()


    # スクレイピング結果を配列で取得する
    result_array = scraping.infected_people_scraping()
    # 現在時刻を配列に追加する
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    date = yesterday.strftime("%Y年%m月%d日")
    weekday = yesterday.weekday()
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    yesterday_date = date + "(" + weekdays[weekday] + ")"
    result_array.append(yesterday_date)
    print(result_array)
    
    sql = "INSERT INTO infected_people (new_people, severe_people, deaths, created_at) VALUES (?, ?, ?, ?)"
    # データベースにデータを格納する
    cur.execute(sql, result_array)
    con.commit

    cur.execute("SELECT * FROM infected_people")
    count = len(cur.fetchall())
    if count > 7:
        first_data = ""
        sql = "SELECT * FROM infected_people LIMIT 1"
        for row in cur.execute(sql):
            first_data = str(row[0])
        cur.execute("DELETE FROM infected_people WHERE id = ?" , (first_data,))
        con.commit()

    cur.close()
    con.close()

# テーブル確認
def print_data():
    db_name = 'infected_people.db'
    # データベースを作成する
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    sql = "SELECT * FROM infected_people"
    for row in cur.execute(sql):
        print_row = [row[4], "新規感染者：" + str(row[1]) + "人", "重症者：" + str(row[2]) + "人", "死亡者：" + str(row[3]) + "人"]
        print(print_row)

    cur.close()
    con.close()


    # 最新の感染情報だけを取得して返す
def print_new_data():
    db_name = 'infected_people.db'
    # データベースを作成する
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    new_data = []
    sql = "SELECT * FROM infected_people LIMIT 7"
    for row in cur.execute(sql):
        new_data = [row[4], "新規感染者：" + str(row[1]) + "人", "重症者：" + str(row[2]) + "人", "死亡者：" + str(row[3]) + "人"]

    cur.close()
    con.close()

    return new_data

def print_week_data():
    db_name = 'infected_people.db'
    # データベースを作成する
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    week_data = []
    sql = "SELECT * FROM infected_people"
    for row in cur.execute(sql):
        week_data.append(row[4] + "\n" + "    新規感染者：" + str(row[1]) + "人" + "\n" + "    重症者：" + str(row[2]) + "人" + "\n" + "    死亡者：" + str(row[3]) + "人")

    cur.close()
    con.close()

    return week_data


# create_db()

# print_data()
# print('----------------------')
# print(print_new_data())
# print('----------------------')
# insert_data()
# print_data()
# print('----------------------')
# print(print_new_data())

# print(print_week_data()[1])