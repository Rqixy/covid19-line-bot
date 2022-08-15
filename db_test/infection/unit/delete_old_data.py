from db_test.infection.unit.first_data import first_data_id

# レコードが7個より大きくなったら一番古いレコードを削除する
def delete_old_data(curs):
    curs.execute("SELECT * FROM test_table;")
    records = curs.fetchall()
    counts = len(records)
    if counts > 7:
        curs.execute("DELETE FROM test_table WHERE id = %s" , (first_data_id(curs),))