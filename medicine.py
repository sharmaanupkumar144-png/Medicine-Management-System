
import sqlite3
from database import connect_db

# 1. Add Medicine
def add_medicine():
    print("\n====================================== ADD MEDICINE ================================")
    conn = None
    try:
        mid = int(input("Medicine ID: "))
        name = input("Medicine Name: ").strip()
        manufacturer = input("Manufacturer: ").strip()
        expiry = input("Expiry Date (DD/MM/YYYY): ").strip()
        price = float(input("Price: "))
        qty = int(input("Quantity: "))
        reorder = int(input("Reorder Level: "))

        if not name or not manufacturer or not expiry:
            print("Fields cannot be empty.")
            return
        if price < 0 or qty < 0 or reorder < 0:
            print("Values cannot be negative.")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO medicines
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (mid, name, manufacturer, expiry,
              price, qty, reorder))
        conn.commit()
        print("Medicine added successfully!")

    except ValueError:
        print("Enter valid numeric values.")
    except sqlite3.IntegrityError:
        print("Medicine ID already exists.")
    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()

# 2. Display Medicines
def display_medicines():
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM medicines ORDER BY medicine_id
        """)
        rows = cur.fetchall()

        print("\n" + "=" * 85)
        print("                             MEDICINES INVENTORY RECORDS")
        print("=" * 85)

        if not rows:
            print("No medicines found.")
            return

        print(f"{'ID':<5}{'Name':<18}{'Manufacturer':<17}"
              f"{'Expiry':<13}{'Price':>8}{'Qty':>7}"
              f"{'Reorder':>9}")
        print("-" * 85)

        for m in rows:
            print(f"{m[0]:<5}{m[1][:17]:<18}"
                  f"{m[2][:16]:<17}{m[3]:<13}"
                  f"{m[4]:>8.2f}{m[5]:>7}{m[6]:>9}")

        print("-" * 85)
        print("Total Records:", len(rows))

    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()

# 3. Search Medicine
def search_medicine():
    print("\n" + "=" * 85)
    print(" " * 30 + "SEARCH MEDICINE")
    print("=" * 85)

    key = input("Enter Medicine ID or Name: ").strip()
    conn = None

    try:
        conn = connect_db()
        cur = conn.cursor()

        if key.isdigit():
            cur.execute(
                "SELECT * FROM medicines WHERE medicine_id = ?",
                (int(key),)
            )
        else:
            cur.execute(
                "SELECT * FROM medicines WHERE name LIKE ?",
                ("%" + key + "%",)
            )

        rows = cur.fetchall()

        print("\n" + "-" * 85)
        print(
            f"{'ID':<6}{'Name':<18}{'Manufacturer':<18}"
            f"{'Expiry Date':<15}{'Price':>10}{'Qty':>8}"
        )
        print("-" * 85)

        if not rows:
            print("Medicine not found.")
        else:
            for m in rows:
                print(
                    f"{m[0]:<6}{m[1][:17]:<18}"
                    f"{m[2][:17]:<18}{m[3]:<15}"
                    f"{m[4]:>10.2f}{m[5]:>8}"
                )

            print("-" * 85)
            print("Total Records:", len(rows))

    except sqlite3.Error as e:
        print("Database Error:", e)

    finally:
        if conn:
            conn.close()

# 4. Update Medicine
def update_medicine():
    print("\n================================== Update Medicine ==================================")
    conn = None
    try:
        mid = int(input("Enter Medicine ID: "))
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM medicines WHERE medicine_id = ?",
            (mid,)
        )
        med = cur.fetchone()

        if not med:
            print("Medicine not found.")
            return

        fields = {
            "1": ("name", "Name", 1, str),
            "2": ("manufacturer", "Manufacturer", 2, str),
            "3": ("expiry_date", "Expiry Date", 3, str),
            "4": ("price", "Price", 4, float),
            "5": ("quantity", "Quantity", 5, int),
            "6": ("reorder_level", "Reorder Level", 6, int)
        }

        while True:
            print("\nMedicine:", med[1])
            print("1. Name          2. Manufacturer")
            print("3. Expiry Date   4. Price")
            print("5. Quantity      6. Reorder Level")
            print("7. Back")

            choice = input("Choose field to update: ").strip()

            if choice == "7":
                break
            if choice not in fields:
                print("Invalid choice.")
                continue

            col, label, index, typ = fields[choice]
            print("Current", label + ":", med[index])

            value = input("New " + label + ": ").strip()
            if not value:
                print("Value cannot be empty.")
                continue

            if typ in (int, float):
                try:
                    value = typ(value)
                except ValueError:
                    print("Enter a valid number.")
                    continue
                if value < 0:
                    print("Value cannot be negative.")
                    continue

            if col == "expiry_date":
                from datetime import datetime
                try:
                    datetime.strptime(value, "%d/%m/%Y")
                except ValueError:
                    print("Use DD/MM/YYYY format.")
                    continue

            cur.execute(
                f"UPDATE medicines SET {col} = ? "
                "WHERE medicine_id = ?",
                (value, mid)
            )
            conn.commit()
            cur.execute(
                "SELECT * FROM medicines WHERE medicine_id = ?",
                (mid,)
            )
            med = cur.fetchone()
            print(label, "updated successfully!")

    except ValueError:
        print("Enter a valid Medicine ID.")
    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()

# 5. Delete Medicine
def delete_medicine():
    print("\n================================= DELETE MEDICINE ====================================")
    conn = None
    try:
        mid = int(input("Enter Medicine ID: "))
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM medicines WHERE medicine_id = ?",
            (mid,)
        )
        med = cur.fetchone()
        if not med:
            print("Medicine not found.")
            return

        print("Medicine:", med[0])
        confirm = input("Delete this medicine? (y/n): ").lower()

        if confirm == "y":
            cur.execute(
                "DELETE FROM medicines WHERE medicine_id = ?",
                (mid,)
            )
            conn.commit()
            print("Medicine deleted successfully!")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Enter a valid Medicine ID.")
    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()


# 6. Restock Medicine
def restock_medicine():
    print("\n================================ RESTOCK MEDICINE ===================================")
    conn = None
    try:
        mid = int(input("Medicine ID: "))
        qty = int(input("Quantity to add: "))

        if qty <= 0:
            print("Quantity must be greater than zero.")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE medicines
            SET quantity = quantity + ?
            WHERE medicine_id = ?
        """, (qty, mid))

        if cur.rowcount == 0:
            print("Medicine not found.")
            return

        conn.commit()
        cur.execute(
            "SELECT name, quantity FROM medicines "
            "WHERE medicine_id = ?", (mid,)
        )
        med = cur.fetchone()

        print("\n--------------- RESTOCK SUCCESSFUL ------")
        print("Medicine:", med[0])
        print("Added Qty:", qty)
        print("Current Stock:", med[1])

    except ValueError:
        print("Enter valid numeric values.")
    except sqlite3.Error as e:
        print("Database Error:", e)
    finally:
        if conn:
            conn.close()
