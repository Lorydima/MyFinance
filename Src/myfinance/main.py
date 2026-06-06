# MyFInance V3.0 Source Code Date: 06/06/2026 Dev LDM Dev

'''
MyFinance is a GUI application designed to facilitate the management of personal finances.

Git Hub Repository Link: "https://github.com/Lorydima/MyFinance"

MyFinance Website link: "https://lorydima.github.io/MyFinance/"

Before you use this code read the license in the LICENSE.txt or on Git Hub Repository.

If you discover a security vulnerability please read the file SECURITY.md on the Git Hub Repository.
'''

# Library for App Dev
import json
import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import webbrowser
import matplotlib.pyplot as plt
import numpy as np


def get_app_dir() -> str:
    """Return the directory that contains the app data files."""

    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Program Assets
APP_DIR = get_app_dir()
DATA_FILE = os.path.join(APP_DIR, "DATA.json")
ICON_FILE = os.path.join(APP_DIR, "MyFinance_Logo.ico")
LICENSE_FILE = os.path.join(APP_DIR, "LICENSE.txt")
VERSION = "3.0"
DATE_DEV = "06/06/2026"
FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 12, "bold")
COLOR_GREEN = "#27ae60"
COLOR_BG = "#4d4d4d"
finance_data = {}
root = None
balance_label = None

# Parse date function
def parse_date(date_str):
    """Safely parse supported date formats and fall back to ``datetime.min``."""

    for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime.min

# Save data function
def save_data():
    """Persist the current finance data to the JSON file."""

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(finance_data, file, indent=4)

# Load data function
def load_data():
    """Load finance data and migrate older records if needed."""

    global finance_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if "currency" not in data:
                    data["currency"] = "€"
                if "transactions" not in data:
                    data["transactions"] = []

                migrated = False
                for transaction in data.get("transactions", []):
                    if transaction.get("type") == "enter":
                        transaction["type"] = "income"
                        migrated = True
                    elif transaction.get("type") == "exit":
                        transaction["type"] = "expense"
                        migrated = True

                    if "date" in transaction:
                        dt = parse_date(transaction["date"])
                        if dt != datetime.min:
                            new_date_str = dt.strftime("%d/%m/%y")
                            if transaction["date"] != new_date_str:
                                transaction["date"] = new_date_str
                                migrated = True

                finance_data = data

                if migrated:
                    save_data()
        except (json.JSONDecodeError, FileNotFoundError):
            finance_data = {"currency": "€", "transactions": []}
    else:
        finance_data = {"currency": "€", "transactions": []}

# Calculate balance function
def calculate_balance():
    """Compute the running balance from all transactions."""

    transactions = finance_data.get("transactions", [])
    values = [float(t["amount"]) if t["type"] == "income" else -float(t["amount"]) for t in transactions]
    return float(np.sum(values)) if values else 0.0

# Update balance display function
def update_balance_display():
    """Refresh the balance label in the main window."""

    if balance_label is None:
        return
    balance = calculate_balance()
    currency = finance_data.get("currency", "€")
    balance_label.config(text=f"Current Balance: {balance:.2f} {currency}")

# Apply icon function
def apply_icon(window):
    """Apply the application icon with a fallback for Linux."""

    try:
        window.iconbitmap(ICON_FILE)
    except Exception:
        try:
            img = tk.PhotoImage(file=ICON_FILE)
            window._myfinance_icon = img  
            window.iconphoto(False, img)
        except Exception:
            pass

# Modal window function
def make_modal(title, geometry):
    """Create a modal window with the shared dark theme."""

    top = tk.Toplevel(root)
    top.title(title)
    top.geometry(geometry)
    top.resizable(False, False)
    top.configure(bg=COLOR_BG)
    top.transient(root)
    top.grab_set()
    apply_icon(top)
    return top

# Show custom info function
def show_custom_info(title, msg):
    """Show a small modal message window."""

    top = make_modal(title, "350x150")
    tk.Label(top, text=msg, font=FONT_BOLD, bg=COLOR_BG, fg="white", wraplength=300).pack(
        expand=True, pady=10
    )
    tk.Button(top, text="OK", command=top.destroy, bg="#f1c40f", fg="black", font=FONT_BOLD, width=10).pack(
        pady=10
    )

# Show license function
def show_license():
    """Display the license file in a scrollable modal."""

    top = make_modal("License", "600x450")
    text_frame = tk.Frame(top, bg=COLOR_BG)
    text_frame.pack(expand=True, fill="both", padx=20, pady=20)

    scrollbar = ttk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_widget = tk.Text(
        text_frame,
        wrap="word",
        bg="#333333",
        fg="white",
        font=FONT_MAIN,
        yscrollcommand=scrollbar.set,
        padx=10,
        pady=10,
        borderwidth=0,
    )
    text_widget.pack(side="left", expand=True, fill="both")
    scrollbar.config(command=text_widget.yview)

    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as file:
            text_widget.insert("1.0", file.read())
    except Exception:
        text_widget.insert("1.0", "License file (LICENSE.txt) not found in the application directory.")

    text_widget.config(state="disabled")
    tk.Button(top, text="Close", command=top.destroy, bg="#f1c40f", fg="black", font=FONT_BOLD, width=10).pack(
        pady=(0, 20)
    )

# Show credits function
def show_credits():
    """Display project credits and useful links."""

    top = make_modal("Credit", "400x420")
    tk.Label(top, text=f"MyFinance V{VERSION}", font=FONT_BOLD, bg=COLOR_BG, fg="white").pack(pady=(20, 10))
    tk.Label(top, text="Dev. LDM Dev", font=FONT_BOLD, bg=COLOR_BG, fg="white").pack(pady=10)

    btn_style = {"bg": "red", "fg": "white", "font": FONT_BOLD, "width": 30, "height": 2}

    tk.Button(
        top,
        text="MyFinance Website",
        command=lambda: webbrowser.open("https://lorydima.github.io/MyFinance"),
        **btn_style,
    ).pack(pady=10)
    tk.Button(
        top,
        text="MyFinance Git Hub Repository",
        command=lambda: webbrowser.open("https://github.com/Lorydima/MyFinance"),
        **btn_style,
    ).pack(pady=10)
    tk.Button(top, text="License", command=show_license, **btn_style).pack(pady=10)

# Change currency function
def change_currency():
    """Open a dialog that lets the user switch currency."""

    top = make_modal("Change Currency", "350x300")
    tk.Label(top, text="Select Currency", font=FONT_BOLD, bg=COLOR_BG, fg="white").pack(pady=20)

    def set_currency(symbol):
        finance_data["currency"] = symbol
        save_data()
        update_balance_display()
        top.destroy()
        show_custom_info("Success", f"Currency changed to {symbol}")

    btn_style = {"bg": "white", "fg": "black", "font": FONT_BOLD, "width": 20, "height": 1}
    tk.Button(top, text="Euro (€)", command=lambda: set_currency("€"), **btn_style).pack(pady=10)
    tk.Button(top, text="Dollar ($)", command=lambda: set_currency("$"), **btn_style).pack(pady=10)
    tk.Button(top, text="Yen (¥)", command=lambda: set_currency("¥"), **btn_style).pack(pady=10)

# Add tansaction function
def add_transaction(transaction_type):
    """Collect and store a new income or expense transaction."""

    dialog = make_modal(f"Add {transaction_type.capitalize()}", "400x350")
    tk.Label(dialog, text=f"New {transaction_type.capitalize()}", font=FONT_BOLD, bg=COLOR_BG, fg="white").pack(
        pady=10
    )

    tk.Label(dialog, text="Description:", bg=COLOR_BG, fg="white", font=FONT_BOLD).pack(pady=(10, 0))
    entry_desc = ttk.Entry(dialog, width=30)
    entry_desc.pack(pady=5)

    tk.Label(dialog, text="Amount:", bg=COLOR_BG, fg="white", font=FONT_BOLD).pack(pady=(10, 0))
    entry_amount = ttk.Entry(dialog, width=30)
    entry_amount.pack(pady=5)

    tk.Label(dialog, text="Date (DD/MM/YYYY):", bg=COLOR_BG, fg="white", font=FONT_BOLD).pack(pady=(10, 0))
    entry_date = ttk.Entry(dialog, width=30)
    entry_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
    entry_date.pack(pady=5)

    def confirm():
        desc = entry_desc.get().strip()
        amount_str = entry_amount.get().strip()
        date_str = entry_date.get().strip()

        if not desc or not amount_str:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            amount = round(float(amount_str), 2)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return

        if parse_date(date_str) == datetime.min:
            messagebox.showerror("Error", "Invalid date format (use DD/MM/YY)")
            return

        new_transaction = {
            "type": transaction_type,
            "amount": amount,
            "description": desc,
            "date": date_str,
        }
        finance_data["transactions"].append(new_transaction)
        finance_data["transactions"].sort(key=lambda x: parse_date(x["date"]), reverse=True)
        save_data()
        update_balance_display()
        dialog.destroy()
        show_custom_info("Success", f"{transaction_type.capitalize()} added!")

    tk.Button(dialog, text="Confirm", command=confirm, bg="#f1c40f", fg="black", font=FONT_BOLD, width=15).pack(
        pady=20
    )


# View transactions function    
def view_transactions():
    """Show all transactions in a tree view."""

    top = make_modal("Transactions History", "900x400")

    style = ttk.Style(top)
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="white",
        foreground="white",
        fieldbackground=COLOR_BG,
        font=FONT_MAIN,
        rowheight=25,
    )
    style.configure("Treeview.Heading", background="#333333", foreground="white", font=FONT_BOLD)
    style.map("Treeview.Heading", background=[("active", "#333333")], foreground=[("active", "white")])
    style.map("Treeview", background=[("selected", "#333333")], foreground=[("selected", "white")])

    tree = ttk.Treeview(top, columns=("Date", "Type", "Description", "Value"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Type", text="Type")
    tree.heading("Description", text="Description")
    tree.heading("Value", text="Value")

    currency = finance_data.get("currency", "€")
    for transaction in finance_data.get("transactions", []):
        prefix = "+" if transaction["type"] == "income" else "-"
        tree.insert(
            "",
            tk.END,
            values=(
                transaction["date"],
                transaction["type"],
                transaction["description"],
                f"{prefix} {transaction['amount']} {currency}",
            ),
            tags=("row",),
        )

    tree.tag_configure("row", background=COLOR_BG)
    tree.pack(expand=True, fill="both")



# View graphs function      
def view_graphs():
    """Plot the balance evolution over time."""

    transactions = finance_data.get("transactions", [])
    if not transactions:
        messagebox.showwarning("Warning", "No data to plot")
        return

    sorted_transactions = sorted(transactions, key=lambda x: parse_date(x["date"]))
    dates = [t["date"] for t in sorted_transactions]

    balance = 0
    balances = []
    for transaction in sorted_transactions:
        balance += float(transaction["amount"]) if transaction["type"] == "income" else -float(transaction["amount"])
        balances.append(balance)

    fig = plt.figure(figsize=(8, 4))
    fig.canvas.manager.set_window_title("Balance Evolution")
    plt.plot(dates, balances, marker="o", color="green")
    plt.title("Balance Evolution")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



# Build GUI function        
def build_gui():
    """Create the main application window and widgets."""

    global root, balance_label

    root = tk.Tk()
    root.title(f"MyFinance {VERSION}")
    root.geometry("800x550")
    root.resizable(False, False)
    root.configure(bg=COLOR_BG)

    apply_icon(root)

    header_frame = tk.Frame(root, bg=COLOR_BG)
    header_frame.pack(pady=10)

    tk.Label(
        header_frame,
        text="My Finance >_",
        font=("Segoe UI", 48, "bold"),
        fg=COLOR_GREEN,
        bg=COLOR_BG,
    ).pack()

    tk.Label(
        header_frame,
        text=f"version: {VERSION}",
        font=("Segoe UI", 12, "bold"),
        fg="#ecf0f1",
        bg=COLOR_BG,
    ).pack()

    balance_frame = tk.Frame(root, bg=COLOR_GREEN, padx=20, pady=15, relief="flat")
    balance_frame.pack(pady=20, fill="x", padx=100)

    balance_label = tk.Label(
        balance_frame,
        text="Current Balance: 0.00 €",
        font=("Segoe UI", 18, "bold"),
        fg="black",
        bg=COLOR_GREEN,
    )
    balance_label.pack()

    btn_frame = tk.Frame(root, bg=COLOR_BG)
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame,
        text="Add Income",
        font=FONT_BOLD,
        bg="#2ecc71",
        fg="black",
        activebackground="#27ae60",
        command=lambda: add_transaction("income"),
        width=20,
        height=2,
    ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Add Expense",
        font=FONT_BOLD,
        bg="#e74c3c",
        fg="black",
        activebackground="#c0392b",
        command=lambda: add_transaction("expense"),
        width=20,
        height=2,
    ).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="View Graph",
        font=FONT_BOLD,
        bg="#3498db",
        fg="black",
        activebackground="#2980b9",
        command=view_graphs,
        width=20,
        height=2,
    ).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="History",
        font=FONT_BOLD,
        bg="#f1c40f",
        fg="black",
        activebackground="#f39c12",
        command=view_transactions,
        width=20,
        height=2,
    ).grid(row=1, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Credit",
        font=FONT_BOLD,
        bg="white",
        fg="black",
        activebackground="#f0f0f0",
        command=show_credits,
        width=20,
        height=2,
    ).grid(row=2, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Change Currency",
        font=FONT_BOLD,
        bg="#eca11f",
        fg="black",
        activebackground="#d68f1a",
        command=change_currency,
        width=20,
        height=2,
    ).grid(row=2, column=1, padx=10, pady=10)


# Main execution block          
if __name__ == "__main__":
    load_data()
    build_gui()
    update_balance_display()
    root.mainloop()
