import sqlite3

connection = sqlite3.connect("database/store.db")

tables = [
    "categories",
    "products",
    "customers",
    "orders",
    "order_items"
]

print("Database record counts:")
print("-" * 30)

for table in tables:
    count = connection.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table:12} : {count}")

connection.close()