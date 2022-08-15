from db.infection.unit.japanese_to_western_calendar import japanese_calendar_converter

# 新しく取得した日付と、最新のレコードにある日付を比較して
# 最新の日付が取得できているかチェックする
def check_new_infected_info(curs, new_infected_day: str) -> bool:
    sql = "SELECT * FROM infected_people ORDER BY id DESC LIMIT 1;"
    curs.execute(sql)
    latest_infected_info_in_db = curs.fetchall()    # DB内での最新のデータを取得

    # DB内の最新の日付のみ取得
    for infected_info in latest_infected_info_in_db:
        latest_infected_day_in_db = str(infected_info[4])

    # 各日付をdatetime型に変換
    converted_new_infected_day = japanese_calendar_converter(new_infected_day)
    converted_latest_infected_day_in_db = japanese_calendar_converter(latest_infected_day_in_db)

    # DB内の最新の日付と送られてきた日付を比較し、
    # 送られてきた日付がDB内の日付より前の日付か、同じ日付だったらfalseを返す
    if converted_new_infected_day <= converted_latest_infected_day_in_db:
        return False
    
    return True