from sqlite3 import connect

conn = connect("database.db")
conn.execute("CREATE TABLE IF NOT EXISTS pdata(name, surname, phone_num)")
conn.commit()
