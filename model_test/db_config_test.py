import psycopg2
import os

# XXX 終わったら消す！！
DATABASE_URL = "postgres://hrywcubbsumlrp:1d8e9de1654ce9c36b63256d80a2f6128d60b58f6775759074e3467ceab2ebd9@ec2-3-227-195-74.compute-1.amazonaws.com:5432/d3krgubfr1615f"

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