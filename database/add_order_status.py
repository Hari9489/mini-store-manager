import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "store.db"


connection = sqlite3.connect(DATABASE_PATH)

try:
    connection.execute(
        """
        ALTER TABLE orders
        ADD COLUMN status TEXT NOT NULL DEFAULT 'Completed'
        """
    )

    connection.commit()

    print("Order status column added successfully.")

except sqlite3.OperationalError as error:
    print("Database update error:", error)

finally:
    connection.close()