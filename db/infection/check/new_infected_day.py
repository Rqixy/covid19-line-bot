from db.infection.unit.japanese_to_western_calendar import japanese_calendar_converter

# 新しく取得した日付と、最新のレコードにある日付を比較して
# 最新の日付が取得できているかチェックする
def check_new_infected_info(curs, new_infected_day: str) -> bool:
    sql = "SELECT * FROM infected_info ORDER BY id DESC LIMIT 1;"
    curs.execute(sql)
    latest_infected_info_in_db = curs.fetchall()    # DB内での最新のデータを取得

    # DB内の最新の日付のみ取得
    for infected_info in latest_infected_info_in_db:
        latest_infected_day_in_db = infected_info[1]

    # 和暦の日付を西暦の日付のdatetime型に変換
    date_new_infected_day = japanese_calendar_converter(new_infected_day)
    date_latest_infected_day_in_db = japanese_calendar_converter(latest_infected_day_in_db)

    # DB内の最新の日付と新しく送られてきた日付を比較し、
    # 新しく送られてきた日付がDB内の日付より前の日付か、同じ日付だったらfalseを返す
    if date_new_infected_day <= date_latest_infected_day_in_db:
        return False
    
    return True