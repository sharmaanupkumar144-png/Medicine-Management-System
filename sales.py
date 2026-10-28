
import sqlite3
from datetime import datetime
from database import connect_db

# 1. Sell Medicine
def sell_medicine():
    print("\n" + "=" * 60)
    print(" " * 22 + "SELL MEDICINE")
    print("=" * 60)
    conn = None
    try:
        mid = int(input("Medicine ID: "))
        qty = int(input("Quantity to Sell: "))
        customer = input("Customer Name: ").strip()
        date = input("Sale Date (DD/MM/YYYY, blank for today): ").strip()
        if not date:
            date = datetime.now().strftime("%d/%m/%Y")
        else:
            datetime.strptime(date, "%d/%m/%Y")
        if qty <= 0:
            print("Quantity must be greater than zero.")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT name, price, quantity FROM medicines WHERE medicine_id = ?",
            (mid,)
        )
        med = cur.fetchone()
        if not med:
            print("Medicine not found.")
            return
        name, price, stock = med
        if qty > stock:
            print("Insufficient stock!")
            print("Available Quantity:", stock)
            return
        total = price * qty
        customer = customer or "Walk-in Customer"
        cur.execute("""
            INSERT INTO sales
            (medicine_id, medicine_name, quantity_sold,
             sale_date, total_amount, customer_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (mid, name, qty, date, total, customer))
        cur.execute(
            "UPDATE medicines SET quantity = quantity - ? WHERE medicine_id = ?",
            (qty, mid)
        )
        conn.commit()
        print("\n" + "=" * 50)
        print(" " * 16 + "SALE RECEIPT")
        print("=" * 50)
        print(f"{'Sale Date':<20}: {date}")
        print(f"{'Customer':<20}: {customer}")
        print(f"{'Medicine':<20}: {name}")
        print(f"{'Quantity':<20}: {qty}")
        print(f"{'Price':<20}: Rs. {price:.2f}")
        print("-" * 50)
        print(f"{'Total Amount':<20}: Rs. {total:.2f}")
        print(f"{'Remaining Stock':<20}: {stock - qty}")
        print("*********************SALE SUCCESSFUL**********************")
    except ValueError:
        print("Enter valid numbers and date in DD/MM/YYYY format.")
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()


# 2. Display Sales
def display_sales():
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT sale_id, medicine_name, quantity_sold,
                   sale_date, total_amount, customer_name
            FROM sales ORDER BY sale_id ASC
        """)
        rows = cur.fetchall()
        print("\n" + "=" * 100)
        print("                                        SALES RECORDS")
        print("=" * 100)
        print(
            f"{'Sale ID':<10} {'Medicine':<20} {'Quantity':>10}  "
            f"{'Sale Date':<15} {'Amount':>12}  {'Customer':<20}"
        )
        print("-" * 100)
        if not rows:
            print("No sales records found.")
            return
        for s in rows:
            customer = s[5] or "Walk-in"
            print(
                f"{s[0]:<10} {s[1][:19]:<20} {s[2]:>10}  "
                f"{s[3]:<15} {s[4]:>12.2f}  {customer[:19]:<20}"
            )
        print("-" * 100)
        print("Total Sales Records:", len(rows))
        print(f"Total Revenue: Rs. {sum(s[4] for s in rows):.2f}")
        print("=" * 100)
    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()


# 3. Cancel Sale
def cancel_sale():
    conn = None
    try:
        sale_id = int(input("Enter Sale ID to cancel: "))
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT medicine_id, medicine_name, quantity_sold,
                   sale_date, total_amount, customer_name
            FROM sales WHERE sale_id = ?
        """, (sale_id,))
        sale = cur.fetchone()
        if not sale:
            print("Sale record not found.")
            return
        mid, name, qty, date, total, customer = sale
        print("\n" + "=" * 60)
        print(" " * 20 + "SALE DETAILS")
        print("=" * 60)
        print("Sale ID:", sale_id)
        print("Medicine:", name)
        print("Quantity Sold:", qty)
        print("Sale Date:", date)
        print(f"Total Amount: Rs. {total:.2f}")
        print("Customer:", customer or "Walk-in Customer")
        print("=" * 60)
        confirm = input("Are you sure you want to cancel this sale? (y/n): ").strip().lower()
        if confirm != "y":
            print("Sale cancellation aborted.")
            return
        cur.execute(
            "UPDATE medicines SET quantity = quantity + ? WHERE medicine_id = ?",
            (qty, mid)
        )
        if cur.rowcount == 0:
            conn.rollback()
            print("Medicine record not found. Sale was not cancelled.")
            return
        cur.execute("DELETE FROM sales WHERE sale_id = ?", (sale_id,))
        conn.commit()
        print("Sale cancelled successfully.")
        print("Medicine stock has been restored.")
    except ValueError:
        print("Please enter a valid Sale ID.")
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()
