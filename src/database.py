import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "store.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    # Return rows that can be accessed by column name
    connection.row_factory = sqlite3.Row

    # Make sure foreign-key constraints are enforced
    connection.execute("PRAGMA foreign_keys = ON")

    return connection