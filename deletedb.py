import sqlite3

db = sqlite3.connect("level.db")

cursor = db.execute("DELETE FROM users")

db.commit()

db.close()

exit()
