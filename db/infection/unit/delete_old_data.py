import db.infection.unit.first_data as FD

# レコードが7個より大きくなったら一番古いレコードを削除する
def delete_old_data(curs):
    curs.execute("SELECT * FROM infected_people;")
    records = curs.fetchall()
    counts = len(records)
    if counts > 7:
        curs.execute("DELETE FROM infected_people WHERE id = %s" , (FD.first_data_id(curs),))