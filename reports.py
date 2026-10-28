
import sqlite3
from datetime import datetime
from database import connect_db

# 1. Sales Summary
def sales_summary():
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM sales")
        result = cur.fetchone()
        print("\n" + "=" * 100)
        print("                                        SALES SUMMARY")
        print("=" * 100)
        print("Total Sales Records:", result[0])
        print(f"Total Revenue: Rs. {result[1]:.2f}")
        print("=" * 100)
    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()

# 2. Low Stock Report
def low_stock_report():
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT medicine_id, name, quantity, reorder_level
            FROM medicines
            WHERE quantity <= reorder_level
            ORDER BY medicine_id
        """)
        rows = cur.fetchall()
        print("\n" + "=" * 100)
        print("                                        LOW STOCK REPORT")
        print("=" * 100)
        print(f"{'ID':<10}{'Medicine Name':<30}{'Quantity':>15}{'Reorder Level':>20}")
        print("-" * 100)
        if not rows:
            print("No low-stock medicines found.")
        else:
            for m in rows:
                print(f"{m[0]:<10}{m[1][:29]:<30}{m[2]:>15}{m[3]:>20}")
        print("=" * 100)
    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()

# 3. Expired Medicines Report
def expired_medicines():
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT medicine_id, name, expiry_date, quantity
            FROM medicines
            ORDER BY medicine_id
        """)
        rows = cur.fetchall()
        today = datetime.now().date()
        expired = []
        for m in rows:
            try:
                expiry = datetime.strptime(m[2], "%d/%m/%Y").date()
                if expiry < today:
                    expired.append(m)
            except ValueError:
                continue
        print("\n" + "=" * 100)
        print("                                     EXPIRED MEDICINES REPORT")
        print("=" * 100)
        print(f"{'ID':<10}{'Medicine Name':<30}{'Expiry Date':<20}{'Quantity':>15}")
        print("-" * 100)
        if not expired:
            print("No expired medicines found.")
        else:
            for m in expired:
                print(f"{m[0]:<10}{m[1][:29]:<30}{m[2]:<20}{m[3]:>15}")
        print("=" * 100)
    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()
