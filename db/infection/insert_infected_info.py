import env
import psycopg2
from db.infection.check.new_infected_day import check_new_infected_info
from db.infection.oneday_infected_info import oneday_infected_info
from db.infection.unit.delete_oldest_info import delete_oldest_info
from scraping.infected_info_scraping import infected_info_scraping


# 感染者情報の追加
def insert_infected_info() -> (list | str):
    # スクレイピングを行い、配列で感染情報を取得する
    infected_info = infected_info_scraping()

    # スクレイピングで情報が正しく取得できていなかったら情報を取得できなかったことを送信する
    if infected_info == None:
        error_text = "情報が正しく取得されませんでした\n午後6時にもう一度送信されます！"
        return error_text

    # 情報が取得されていたら、変数に格納する
    infected_day = infected_info[0]
    new_infected_people = infected_info[1]
    severe_people = infected_info[2]
    deaths = infected_info[3]

    # データベースに接続する
    with psycopg2.connect(env.DATABASE_URL) as conn:
        with conn.cursor() as curs:
            # もし新しいデータが入ってこなかったら新しいデータが無いことを送信する
            if not check_new_infected_info(curs, infected_day):
                error_text = "新しい感染者情報が更新されていません！\n午後6時にもう一度送信されます！"
                return error_text

            # スクレイピングで取ってきた配列のデータを格納する
            sql = "INSERT INTO infected_info (infected_day, new_infected_people, severe_people, deaths) VALUES (%s, %s, %s, %s)"
            curs.execute(sql, (infected_day, new_infected_people, severe_people, deaths))

            # レコードが7個より大きくなったら一番古いレコードを削除する
            delete_oldest_info(curs)

    # 新しいデータが更新されたら最新情報を表示する
    new_infected_info = oneday_infected_info(0)

    return new_infected_info
