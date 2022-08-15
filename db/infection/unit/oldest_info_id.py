# 一番古いレコードを削除するためのid取得をして返す
def oldest_info_id(curs):
    sql = "SELECT * FROM infected_people ORDER BY id LIMIT 1;"
    curs.execute(sql)
    records = curs.fetchall()
    first_data_id = ""
    for row in records:
        first_data_id = str(row[0])
    return first_data_id