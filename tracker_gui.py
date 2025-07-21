import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

DATA_FILE = "data.csv"

# Function to add entry
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

def clear_fields():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

# --- GUI Setup ---
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("400x300")

# Entry Type
type_var = tk.StringVar(value="Expense")
tk.Label(root, text="Type:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.OptionMenu(root, type_var, "Expense", "Income").grid(row=0, column=1, pady=5, sticky="w")

# Category
tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, pady=5)

# Amount
tk.Label(root, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, pady=5)

# Description
tk.Label(root, text="Description:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
desc_entry = tk.Entry(root)
desc_entry.grid(row=3, column=1, pady=5)

# Add Button
tk.Button(root, text="Add Entry", command=add_entry, bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
