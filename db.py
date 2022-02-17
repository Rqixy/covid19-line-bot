import scraping
import sqlite3
from datetime import datetime


# データベース作成
def create_db():
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

# データの追加
def insert_data():
    db_name = 'infected_people.db'
    # データベースを作成する
    con = sqlite3.connect(db_name)
    cur = con.cursor()


    # スクレイピング結果を配列で取得する
    result_array = scraping.infected_people_scraping()
    # 現在時刻を配列に追加する
    now = datetime.now().isoformat()
    result_array.append(now)
    # print(result_array)
    
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
        print(row)

    cur.close()
    con.close()




# create_db()
print_data()

insert_data()


# create_db()
print_data()