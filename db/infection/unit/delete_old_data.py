from db.infection.unit.first_data import first_data_id

# レコードが7個より大きくなったら一番古いレコードを削除する
def delete_oldest_info(curs):
    curs.execute("SELECT * FROM infected_people;")
    records = curs.fetchall()
    counts = len(records)
    if counts > 7:
        curs.execute("DELETE FROM infected_people WHERE id = %s" , (first_data_id(curs),))