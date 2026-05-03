import sqlite3
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

DB = "expenses.db"

# ---------- INIT DB ---------- #
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    type TEXT
                )''')
    conn.commit()
    conn.close()

# ---------- ADD ENTRY ---------- #
def add_entry():
    date = date_entry.get()
    category = category_entry.get()
    
    try:
        amount = float(amount_entry.get())
    except:
        messagebox.showerror("Error", "Invalid amount")
        return

    t = type_var.get()

    if not date or not category:
        messagebox.showerror("Error", "All fields required")
        return

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO records (date, category, amount, type) VALUES (?, ?, ?, ?)",
              (date, category, amount, t))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Entry Added!")

# ---------- SUMMARY ---------- #
def summary():
    month = month_entry.get()

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT type, SUM(amount) FROM records WHERE date LIKE ? GROUP BY type",
              (month + '%',))
    data = c.fetchall()
    conn.close()

    income = 0
    expense = 0

    for row in data:
        if row[0] == "income":
            income = row[1] or 0
        elif row[0] == "expense":
            expense = row[1] or 0

    result = f"Income: {income}\nExpense: {expense}\nBalance: {income - expense}"
    messagebox.showinfo("Summary", result)

# ---------- CHART ---------- #
def show_chart():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT category, SUM(amount) FROM records WHERE type='expense' GROUP BY category")
    data = c.fetchall()
    conn.close()

    if not data:
        messagebox.showerror("Error", "No data!")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure()
    plt.bar(categories, amounts)
    plt.title("Expenses by Category")
    plt.xticks(rotation=30)

    plt.savefig("chart.png")
    plt.show()

# ---------- UI ---------- #
root = tk.Tk()
root.title("Expense Tracker")

# Inputs
tk.Label(root, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Type").pack()
type_var = tk.StringVar(value="expense")
tk.OptionMenu(root, type_var, "income", "expense").pack()

# Month for summary
tk.Label(root, text="Month (YYYY-MM)").pack()
month_entry = tk.Entry(root)
month_entry.pack()

# Buttons
tk.Button(root, text="Add Entry", command=add_entry).pack(pady=5)
tk.Button(root, text="Monthly Summary", command=summary).pack(pady=5)
tk.Button(root, text="Show Chart", command=show_chart).pack(pady=5)

# Run
init_db()
root.mainloop()