from db.infection.unit.oldest_info_id import oldest_info_id

# レコードが7個より大きくなったら一番古いレコードを削除する
def delete_oldest_info(curs):
    curs.execute("SELECT * FROM infected_people;")
    records = curs.fetchall()
    record_counts = len(records)   # DB内のレコード数を数える
    
    if record_counts > 7:
        curs.execute("DELETE FROM infected_people WHERE id = %s" , (oldest_info_id(curs),))