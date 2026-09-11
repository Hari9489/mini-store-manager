import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "store.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

connection = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
    schema = file.read()

connection.executescript(schema)
connection.commit()
connection.close()

print(f"Database created successfully: {DB_PATH}")