import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

# File paths
DATA_FILE = 'expenses.json'

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Add an expense
def add_expense():
    date = simpledialog.askstring("Input", "Enter date (YYYY-MM-DD):")
    category = simpledialog.askstring("Input", "Enter category (e.g., food, transport):")
    amount = simpledialog.askfloat("Input", "Enter amount:")
    
    if date and category and amount is not None:
        expense_id = len(expenses) + 1
        expenses[expense_id] = {'date': date, 'category': category, 'amount': amount}
        save_data(expenses)
        refresh_expense_list()
        messagebox.showinfo("Success", "Expense added successfully.")
    else:
        messagebox.showerror("Error", "Invalid input. Please try again.")

# View all expenses
def view_expenses():
    expenses_text = ""
    if not expenses:
        expenses_text = "No expenses recorded."
    else:
        for expense_id, details in expenses.items():
            expenses_text += f"ID: {expense_id}, Date: {details['date']}, Category: {details['category']}, Amount: ${details['amount']:.2f}\n"
    
    messagebox.showinfo("Expenses", expenses_text)

# Delete an expense
def delete_expense():
    expense_id = simpledialog.askinteger("Input", "Enter the ID of the expense to delete:")
    if expense_id in expenses:
        del expenses[expense_id]
        save_data(expenses)
        refresh_expense_list()
        messagebox.showinfo("Success", "Expense deleted successfully.")
    else:
        messagebox.showerror("Error", "Expense ID not found.")

# Refresh the expense list display
def refresh_expense_list():
    expenses_list.delete(1.0, tk.END)
    if expenses:
        for expense_id, details in expenses.items():
            expenses_list.insert(tk.END, f"ID: {expense_id}, Date: {details['date']}, Category: {details['category']}, Amount: ${details['amount']:.2f}\n")

# Main application window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")
root.configure(bg='#f4f4f4')

# Create a style for buttons and text widgets
style = ttk.Style()
style.configure("TButton",
                padding=14,
                relief="flat",
                background="skyblue",
                foreground="black",
                font=("sans-serif", 16, "bold"))
style.map("TButton",
          background=[('active', 'black')],
          foreground=[('active', 'blue')])

style.configure("TText",
                padding=10,
                relief="flat",
                background="white",
                foreground="black",
                font=("Helvetica", 16))
style.configure("TLabel",
                background="black",
                foreground="white",
                font=("Helvetica", 16, "bold"))

# Header Label
header_label = tk.Label(root, text="Expense Tracker", font=("Helvetica", 18, "bold"), bg='skyblue', fg='blue', pady=10)
header_label.pack(fill=tk.X)

# Add Expense Button
add_button = ttk.Button(root, text="Add Expense", command=add_expense)
add_button.pack(pady=10, padx=20, side=tk.LEFT)

# View Expenses Button
view_button = ttk.Button(root, text="View Expenses", command=view_expenses)
view_button.pack(pady=10, padx=20, side=tk.LEFT)

# Delete Expense Button
delete_button = ttk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.pack(pady=10, padx=20, side=tk.LEFT)

# Text widget to display expenses
expenses_list = tk.Text(root, width=85, height=20, wrap=tk.WORD, font=("Helvetica", 12), bg="skyblue", fg="#333333", borderwidth=2, relief="ridge")
expenses_list.pack(pady=40, padx=40)

# Load existing data and refresh the list
expenses = load_data()
print("Expenses loaded:", expenses)  # Debugging print
refresh_expense_list()

# Start the GUI event loop
root.mainloop()
