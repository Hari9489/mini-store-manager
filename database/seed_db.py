import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "store.db"
SEED_PATH = BASE_DIR / "seed.sql"

connection = sqlite3.connect(DB_PATH)

try:
    with open(SEED_PATH, "r", encoding="utf-8") as file:
        seed = file.read()

    connection.executescript(seed)
    connection.commit()

    print("Seed data inserted successfully.")

except sqlite3.Error as error:
    connection.rollback()
    print(f"Database error: {error}")

finally:
    connection.close()