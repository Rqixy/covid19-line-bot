import os
import sys
import psycopg2
import db_test.config as config
import print_day as PD
import db_test.infection.unit.delete_old_data as DOD
sys.path.append(os.path.join(os.path.dirname(__file__), '../scraping_test'))
import scraping_test.infected_people as scraping

db_url = config.DATABASE_URL

# 感染者データの追加
def insert_infected_data():
    # スクレイピングを行い、配列で取得する
    infected_info = scraping.infected_people_scraping()

    # スクレイピングで情報が取得できていなかったら情報を取得できなかったことを送信する
    if infected_info == None:
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
            if result == infected_info[0]:
                text = "新しい感染者情報が更新されていません！\n午後6時にもう一度送信されます！"
                return text

            # スクレイピングで取ってきた配列のデータを格納する
            sql = "INSERT INTO test_table (new_people, severe_people, deaths, infected_day) VALUES (%s, %s, %s, %s)"
            curs.execute(sql, (infected_info[1], infected_info[2], infected_info[3], infected_info[0]))

            # レコードが7個より大きくなったら一番古いレコードを削除する
            DOD.delete_old_data(curs)

            # 新しいデータが更新されたら最新情報を表示する
            new_data = PD.print_infected_day(0)

            return new_data