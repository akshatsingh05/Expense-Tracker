import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

DATA_FILE = "data.csv"

# ------------------ Add Entry Function ------------------
def add_entry():
    date = datetime.today().strftime('%Y-%m-%d')
    entry_type = type_var.get().capitalize()
    category = category_entry.get().title()
    amount = amount_entry.get()
    description = desc_entry.get()

    if not category or not amount or not description:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    row = [date, entry_type, category, amount, description]
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["date", "type", "category", "amount", "description"])
        writer.writerow(row)

    messagebox.showinfo("Success", "Entry added successfully!")
    clear_fields()
    load_entries()  # Refresh table after adding entry

def clear_fields():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

# ------------------ Load Entries into Table ------------------
def load_entries():
    for row in table.get_children():
        table.delete(row)

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            table.insert("", tk.END, values=row)

# ------------------ GUI Setup ------------------
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("600x400")

# Create Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# ------------------ Tab 1: Add Entry ------------------
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Add Entry")

type_var = tk.StringVar(value="Expense")
ttk.Label(tab1, text="Type:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
ttk.OptionMenu(tab1, type_var, "Expense", "Income").grid(row=0, column=1, pady=5, sticky="w")

ttk.Label(tab1, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
category_entry = ttk.Entry(tab1)
category_entry.grid(row=1, column=1, pady=5)

ttk.Label(tab1, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
amount_entry = ttk.Entry(tab1)
amount_entry.grid(row=2, column=1, pady=5)

ttk.Label(tab1, text="Description:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
desc_entry = ttk.Entry(tab1)
desc_entry.grid(row=3, column=1, pady=5)

ttk.Button(tab1, text="Add Entry", command=add_entry).grid(row=4, column=0, columnspan=2, pady=10)

# ------------------ Tab 2: View Entries ------------------
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="View Entries")

# Create Treeview Table
columns = ("Date", "Type", "Category", "Amount", "Description")
table = ttk.Treeview(tab2, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=100, anchor="center")
table.pack(expand=True, fill="both", padx=10, pady=10)

# Load entries when program starts
load_entries()

root.mainloop()
