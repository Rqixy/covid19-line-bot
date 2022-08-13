import psycopg2
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