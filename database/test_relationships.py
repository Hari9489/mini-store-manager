import sqlite3

connection = sqlite3.connect("database/store.db")
connection.execute("PRAGMA foreign_keys = ON")

print("Foreign key violations:")
violations = connection.execute(
    "PRAGMA foreign_key_check"
).fetchall()

if violations:
    for violation in violations:
        print(violation)
else:
    print("None - all foreign keys are valid.")

connection.close()