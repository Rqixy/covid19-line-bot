# 一番古いレコードを削除するためのid取得をして返す
def oldest_info_id(curs) -> str:
    sql = "SELECT * FROM infected_info ORDER BY id LIMIT 1;"
    curs.execute(sql)
    for infected_info in curs.fetchall():
        oldest_id = str(infected_info[0])

    return oldest_id