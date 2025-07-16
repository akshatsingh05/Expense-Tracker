import csv
from datetime import datetime
import os

DATA_FILE = "data.csv"

def add_entry():
    date = datetime.today().strftime('%Y-%m-%d')
    entry_type = input("Enter type (Income/Expense): ").strip().capitalize()
    category = input("Enter category (e.g. Food, Salary): ").strip().title()

    while True:
        try:
            amount = float(input("Enter amount: ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")

    description = input("Enter description: ").strip()
    row = [date, entry_type, category, amount, description]

    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["date", "type", "category", "amount", "description"])
        writer.writerow(row)

    print("\n✅ Entry saved successfully!\n")

def view_entries():
    if not os.path.exists(DATA_FILE):
        print("\n⚠️ No data found. Add some entries first.\n")
        return

    with open(DATA_FILE, mode="r") as file:
        reader = csv.reader(file)
        entries = list(reader)

    if len(entries) <= 1:
        print("\n⚠️ No data to display.\n")
        return

    print("\n📋 Transaction History:\n")
    print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<10} Description")
    print("-" * 65)

    for row in entries[1:]:  # Skip header
        date, typ, cat, amt, desc = row
        print(f"{date:<12} {typ:<10} {cat:<15} {amt:<10} {desc}")

    print()

def filter_by_category():
    if not os.path.exists(DATA_FILE):
        print("\n⚠️ No data found. Add some entries first.\n")
        return

    category_input = input("Enter category to filter by (e.g. Food): ").strip().title()

    with open(DATA_FILE, mode="r") as file:
        reader = csv.reader(file)
        entries = list(reader)

    if len(entries) <= 1:
        print("\n⚠️ No data to filter.\n")
        return

    filtered = [row for row in entries[1:] if row[2] == category_input]  # index 2 is 'category'

    if not filtered:
        print(f"\n❌ No entries found for category: {category_input}\n")
        return

    print(f"\n📂 Entries in category '{category_input}':\n")
    print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<10} Description")
    print("-" * 65)

    for row in filtered:
        date, typ, cat, amt, desc = row
        print(f"{date:<12} {typ:<10} {cat:<15} {amt:<10} {desc}")

    print()

def monthly_summary():
    if not os.path.exists(DATA_FILE):
        print("\n⚠️ No data found. Add some entries first.\n")
        return

    month_input = input("Enter month number (e.g. 07 for July): ").strip().zfill(2)

    with open(DATA_FILE, mode="r") as file:
        reader = csv.reader(file)
        entries = list(reader)

    if len(entries) <= 1:
        print("\n⚠️ No data to summarize.\n")
        return

    income_total = 0
    expense_total = 0
    matched_entries = []

    for row in entries[1:]:
        date, typ, category, amount, description = row
        entry_month = date.split("-")[1]  # Extract month

        if entry_month == month_input:
            matched_entries.append(row)
            if typ == "Income":
                income_total += float(amount)
            elif typ == "Expense":
                expense_total += float(amount)

    if not matched_entries:
        print(f"\n❌ No entries found for month {month_input}\n")
        return

    print(f"\n📆 Transactions in Month {month_input}:\n")
    print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<10} Description")
    print("-" * 65)

    for row in matched_entries:
        date, typ, cat, amt, desc = row
        print(f"{date:<12} {typ:<10} {cat:<15} {amt:<10} {desc}")

    # 🔽 Monthly Totals and Summary
    print("-" * 65)
    print(f"\n💰 Total Income  : ₹ {income_total:.2f}")
    print(f"💸 Total Expense : ₹ {expense_total:.2f}")
    print(f"📊 Net Balance   : ₹ {income_total - expense_total:.2f}\n")



def menu():
    while True:
        print("=== Personal Expense Tracker ===")
        print("1. Add Entry")
        print("2. View All Entries")
        print("3. Exit")
        print("4. View by Category")
        print("5. Monthly Summary")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            print("Goodbye!")
            break
        elif choice == "4":
            filter_by_category()
        elif choice == "5":
            monthly_summary()
        else:
            print("❌ Invalid option. Try again.\n")


if __name__ == "__main__":
    menu()
