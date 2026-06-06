"""Tkinter GUI for MyFinance."""

from __future__ import annotations

import webbrowser
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
import numpy as np

from .config import COLOR_BG, COLOR_GREEN, FONT_BOLD, FONT_MAIN, ICON_FILE, LICENSE_FILE, VERSION
from .storage import load_data, parse_date, save_data


class MyFinanceApp:
    """Main GUI application for MyFinance."""

    def __init__(self) -> None:
        self.finance_data = load_data()
        self.root = tk.Tk()
        self.balance_label: tk.Label | None = None

        self.root.title(f"MyFinance {VERSION}")
        self.root.geometry("800x550")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        self._apply_icon(self.root)
        self._build_layout()
        self.update_balance_display()

    def _apply_icon(self, window: tk.Tk | tk.Toplevel) -> None:
        """Attach the app icon to a window, using platform-specific fallbacks."""

        try:
            window.iconbitmap(str(ICON_FILE))
        except Exception:
            try:
                # Keep a reference so Tk does not garbage-collect the image.
                image = tk.PhotoImage(file=str(ICON_FILE))
                window._myfinance_icon = image  # type: ignore[attr-defined]
                window.iconphoto(False, image)
            except Exception:
                pass

    def _make_modal(self, title: str, geometry: str) -> tk.Toplevel:
        """Create a modal dialog window with the shared dark theme."""

        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry(geometry)
        top.resizable(False, False)
        top.configure(bg=COLOR_BG)
        top.transient(self.root)
        top.grab_set()
        self._apply_icon(top)
        return top

    def calculate_balance(self) -> float:
        """Return the current balance from the loaded transaction list."""

        transactions = self.finance_data.get("transactions", [])
        values = [
            float(item["amount"]) if item["type"] == "income" else -float(item["amount"])
            for item in transactions
        ]
        return float(np.sum(values)) if values else 0.0

    def update_balance_display(self) -> None:
        """Refresh the balance label after a data change."""

        if self.balance_label is None:
            return

        balance = self.calculate_balance()
        currency = self.finance_data.get("currency", "€")
        self.balance_label.config(text=f"Current Balance: {balance:.2f} {currency}")

    def show_custom_info(self, title: str, msg: str) -> None:
        """Show a small modal message window used by several actions."""

        top = self._make_modal(title, "350x150")

        tk.Label(
            top,
            text=msg,
            font=FONT_BOLD,
            bg=COLOR_BG,
            fg="white",
            wraplength=300,
        ).pack(expand=True, pady=10)
        tk.Button(
            top,
            text="OK",
            command=top.destroy,
            bg="#f1c40f",
            fg="black",
            font=FONT_BOLD,
            width=10,
        ).pack(pady=10)

    def show_license(self) -> None:
        """Display the license text in a scrollable modal window."""

        top = self._make_modal("License", "600x450")
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
            with LICENSE_FILE.open("r", encoding="utf-8") as file:
                text_widget.insert("1.0", file.read())
        except Exception:
            text_widget.insert(
                "1.0",
                "License file (LICENSE.txt) not found in the application directory.",
            )

        text_widget.config(state="disabled")
        tk.Button(
            top,
            text="Close",
            command=top.destroy,
            bg="#f1c40f",
            fg="black",
            font=FONT_BOLD,
            width=10,
        ).pack(pady=(0, 20))

    def show_credits(self) -> None:
        """Display links to the website, repository, and license."""

        top = self._make_modal("Credit", "400x420")

        tk.Label(top, text=f"MyFinance V{VERSION}", font=FONT_BOLD, bg=COLOR_BG, fg="white").pack(
            pady=(20, 10)
        )
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
        tk.Button(top, text="License", command=self.show_license, **btn_style).pack(pady=10)

    def change_currency(self) -> None:
        """Open a modal to switch the active currency symbol."""

        top = self._make_modal("Change Currency", "350x300")

        tk.Label(top, text="Select Currency", font=FONT_BOLD, bg=COLOR_BG, fg="white").pack(pady=20)

        def set_currency(symbol: str) -> None:
            self.finance_data["currency"] = symbol
            save_data(self.finance_data)
            self.update_balance_display()
            top.destroy()
            self.show_custom_info("Success", f"Currency changed to {symbol}")

        btn_style = {"bg": "white", "fg": "black", "font": FONT_BOLD, "width": 20, "height": 1}

        tk.Button(top, text="Euro (€)", command=lambda: set_currency("€"), **btn_style).pack(pady=10)
        tk.Button(top, text="Dollar ($)", command=lambda: set_currency("$"), **btn_style).pack(pady=10)
        tk.Button(top, text="Yen (¥)", command=lambda: set_currency("¥"), **btn_style).pack(pady=10)

    def add_transaction(self, transaction_type: str) -> None:
        """Collect a transaction from the user and store it in the JSON data."""

        dialog = self._make_modal(f"Add {transaction_type.capitalize()}", "400x350")

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

        def confirm() -> None:
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
            self.finance_data.setdefault("transactions", []).append(new_transaction)
            self.finance_data["transactions"].sort(key=lambda item: parse_date(item["date"]), reverse=True)
            save_data(self.finance_data)
            self.update_balance_display()
            dialog.destroy()
            self.show_custom_info("Success", f"{transaction_type.capitalize()} added!")

        tk.Button(dialog, text="Confirm", command=confirm, bg="#f1c40f", fg="black", font=FONT_BOLD, width=15).pack(
            pady=20
        )

    def view_transactions(self) -> None:
        """Show the transaction list in a simple table window."""

        top = self._make_modal("Transactions History", "900x400")

        style = ttk.Style(top)
        style.theme_use("clam")
        # Keep the table readable against the dark window background.
        style.configure(
            "Treeview",
            background="white",
            foreground="white",
            fieldbackground=COLOR_BG,
            font=FONT_MAIN,
            rowheight=25,
        )
        style.configure("Treeview.Heading", background="#333333", foreground="white", font=FONT_BOLD)
        style.map(
            "Treeview.Heading",
            background=[("active", "#333333")],
            foreground=[("active", "white")],
        )
        style.map(
            "Treeview",
            background=[("selected", "#333333")],
            foreground=[("selected", "white")],
        )

        tree = ttk.Treeview(top, columns=("Date", "Type", "Description", "Value"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Type", text="Type")
        tree.heading("Description", text="Description")
        tree.heading("Value", text="Value")

        currency = self.finance_data.get("currency", "€")
        for transaction in self.finance_data.get("transactions", []):
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

    def view_graphs(self) -> None:
        """Plot the balance evolution over time."""

        transactions = self.finance_data.get("transactions", [])
        if not transactions:
            messagebox.showwarning("Warning", "No data to plot")
            return

        sorted_transactions = sorted(transactions, key=lambda item: parse_date(item["date"]))
        dates: list[str] = []
        balances: list[float] = []
        balance = 0.0

        for transaction in sorted_transactions:
            amount = float(transaction["amount"])
            if transaction["type"] == "income":
                balance += amount
            else:
                balance -= amount
            dates.append(transaction["date"])
            balances.append(balance)

        currency = self.finance_data.get("currency", "€")

        fig = plt.figure(figsize=(8, 4))
        fig.canvas.manager.set_window_title("Balance Evolution")
        plt.plot(dates, balances, marker="o", color="green")
        plt.title("Balance Evolution")
        plt.xticks(rotation=45)
        plt.ylabel(f"Balance ({currency})")
        plt.tight_layout()
        plt.show()

    def _build_layout(self) -> None:
        """Build the main dashboard layout."""

        header_frame = tk.Frame(self.root, bg=COLOR_BG)
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

        balance_frame = tk.Frame(self.root, bg=COLOR_GREEN, padx=20, pady=15, relief="flat")
        balance_frame.pack(pady=20, fill="x", padx=100)

        self.balance_label = tk.Label(
            balance_frame,
            text="Current Balance: 0.00 €",
            font=("Segoe UI", 18, "bold"),
            fg="black",
            bg=COLOR_GREEN,
        )
        self.balance_label.pack()

        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Income",
            font=FONT_BOLD,
            bg="#2ecc71",
            fg="black",
            activebackground="#27ae60",
            command=lambda: self.add_transaction("income"),
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
            command=lambda: self.add_transaction("expense"),
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
            command=self.view_graphs,
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
            command=self.view_transactions,
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
            command=self.show_credits,
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
            command=self.change_currency,
            width=20,
            height=2,
        ).grid(row=2, column=1, padx=10, pady=10)

    def run(self) -> None:
        """Start the Tkinter event loop."""

        self.root.mainloop()

