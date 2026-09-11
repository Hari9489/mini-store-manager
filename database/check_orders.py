import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "store.db"


connection = sqlite3.connect(DATABASE_PATH)

columns = connection.execute(
    "PRAGMA table_info(orders)"
).fetchall()

for column in columns:
    print(column)

connection.close()