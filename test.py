import db
user_id = 'U6db81b1f3a83373e0ee315628b191fb5'
db.insert_user_data(user_id=user_id)

print(db.print_user_id())