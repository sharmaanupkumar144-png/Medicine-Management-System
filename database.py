
import sqlite3

DB_NAME = "medicine.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Medicine table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            medicine_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manufacturer TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            reorder_level INTEGER NOT NULL
        )
    """)

    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER NOT NULL,
            medicine_name TEXT NOT NULL,
            quantity_sold INTEGER NOT NULL,
            sale_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            customer_name TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database and tables created successfully.")


if __name__ == "__main__":
    create_tables()
