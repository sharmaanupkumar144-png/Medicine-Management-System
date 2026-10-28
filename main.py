
from database import create_tables
from medicine import (
    add_medicine, display_medicines, search_medicine,
    update_medicine, delete_medicine, restock_medicine
)
from sales import sell_medicine, display_sales, cancel_sale
from reports import sales_summary, low_stock_report, expired_medicines

def medicine_menu():
    while True:
        print("\n" + "=" * 100)
        print("                                       MEDICINE MODULE")
        print("=" * 100)
        print("1. Add Medicine")
        print("2. Display Medicines")
        print("3. Search Medicine")
        print("4. Update Medicine")
        print("5. Delete Medicine")
        print("6. Restock Medicine")
        print("7. Back to Main Menu")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_medicine()
        elif choice == "2":
            display_medicines()
        elif choice == "3":
            search_medicine()
        elif choice == "4":
            update_medicine()
        elif choice == "5":
            delete_medicine()
        elif choice == "6":
            restock_medicine()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


def sales_menu():
    while True:
        print("\n" + "=" * 100)
        print("                                       SALES MODULE")
        print("=" * 100)
        print("1. Sell Medicine")
        print("2. Display Sales")
        print("3. Cancel Sale")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            sell_medicine()
        elif choice == "2":
            display_sales()
        elif choice == "3":
            cancel_sale()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def reports_menu():
    while True:
        print("\n" + "=" * 100)
        print("                                       REPORTS MODULE")
        print("=" * 100)
        print("1. Sales Summary")
        print("2. Low Stock Report")
        print("3. Expired Medicines Report")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            sales_summary()
        elif choice == "2":
            low_stock_report()
        elif choice == "3":
            expired_medicines()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    create_tables()
    while True:
        print("\n" + "=" * 100)
        print("                                PHARMACY MANAGEMENT SYSTEM")
        print("=" * 100)
        print("1. Medicine Module")
        print("2. Sales Module")
        print("3. Reports")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            medicine_menu()
        elif choice == "2":
            sales_menu()
        elif choice == "3":
            reports_menu()
        elif choice == "4":
            print("\nThank you for using Pharmacy Management System!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
