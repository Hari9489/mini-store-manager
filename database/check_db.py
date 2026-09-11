import sqlite3

connection = sqlite3.connect("database/store.db")

tables = connection.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""").fetchall()

print("Tables in database:")
for table in tables:
    print("-", table[0])

connection.close()