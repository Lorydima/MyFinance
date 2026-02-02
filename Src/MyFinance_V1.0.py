# MyFinance>_ Source Code Date 02/02/2026 Dev: LDM Dev

'''
MyFinance>_ is a finance manager on CLI

Git Hub Repository Link: "https://github.com/Lorydima/MyFinance"

Before you use this code read the license in the LICENSE.txt or on Git Hub Repository.
'''

# Library for App Dev.
from pyfiglet import Figlet
from rich.align import Align
from rich.rule import Rule
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from datetime import datetime
from rich import print
import numpy
import json
import os

# Console 
console = Console()

# Global Data
finance_data = {}

# Load Data Function
def load_data():
    """
    Loads financial data from DATA.json.
    Initializes with default values if the file doesn't exist or is corrupted.
    """
    global finance_data
    if os.path.exists('DATA.json'):
        try:
            with open('DATA.json', 'r') as f:
                data = json.load(f)
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
                
                finance_data = data
                
                if migrated:
                    save_data()

        except (json.JSONDecodeError, FileNotFoundError):
            finance_data = {"currency": "€", "transactions": []}
    else:
        finance_data = {"currency": "€", "transactions": []}

# Introduction
def introduction():
    """Displays the application's title, version, and developer info."""
    f = Figlet(font='standard')
    introduction_title = f.renderText("My Finance >_")
    info_text = "V1.0 Date 02/12/2026 Dev: LDM Dev"

    title = Align.center(f"[green]{introduction_title}[/green]")
    subtitle = Align.center(f"[bold blue]{info_text}[/bold blue]")
    print(title)
    print(subtitle)
    print(Rule(style="white"))
    command_panel()

# Command Panel 
def command_panel():
    """Displays a panel with all available commands."""
    print(
        Panel(
            "[bold][green]Add Income[/green][/bold]"
            "\n[bold][red]Add Expense[/red][/bold]"
            "\n[bold][blue]View Balance[/blue][/bold]"
            "\n[yellow][bold]View all transactions[/yellow][/bold]"
            "\n[bold][cyan]Change Currency[/cyan][/bold]"
            "\n[red]Exit[/red]",
            title="Commands",
            style="green"
        )
    )
    print(Rule(style="white"))
    command_loop()

# View Transactions
def view_transactions():
    """
    Displays a table of all transactions.
    If no transactions are found, it shows a message.
    Calculates and displays the current balance at the end.
    """
    console.print(Rule(style="white"))

    if not finance_data.get("transactions"):
        console.print(Align.center("[yellow]No data saved[/yellow]"))
        console.print(Rule(style="white"))
        return

    table = Table(title="Transactions History", style="yellow")

    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Value", justify="right", style="green")

    currency_symbol = finance_data.get("currency", "€")

    for item in finance_data.get("transactions", []):
        t_type = item["type"]
        amount = item["amount"]
        
        if t_type == "expense":
            type_style = "[red]Expense[/red]"
            amount_style = f"[red]- {amount} {currency_symbol}[/red]"
        else:
            type_style = "[green]Income[/green]"
            amount_style = f"[green]+ {amount} {currency_symbol}[/green]"
            
        table.add_row(item["date"], type_style, item["description"], amount_style)

    console.print(Align.center(table))

    transactions = finance_data.get("transactions", [])
    values = [float(t["amount"]) if t["type"] == "income" else -float(t["amount"]) for t in transactions]
    balance = numpy.sum(values)
    
    console.print(Align.center(f"\n[bold]Current Balance: {balance:.2f} {currency_symbol}[/bold]"))
    console.print(Rule(style="white"))

# View Balance
def view_balance():
    """
    Calculates and displays a summary of total income, total expenses, and the final balance.
    If no transactions are found, it shows a message.
    """
    console.print(Rule(style="white"))
    transactions = finance_data.get("transactions", [])

    if not transactions:
        console.print(Align.center("[yellow]No data saved[/yellow]"))
        console.print(Rule(style="white"))
        return
    
    incomes = [float(t["amount"]) for t in transactions if t["type"] == "income"]
    total_income = numpy.sum(incomes)

    expenses = [float(t["amount"]) for t in transactions if t["type"] == "expense"]
    total_expenses = numpy.sum(expenses)
    
    balance = total_income - total_expenses
    currency_symbol = finance_data.get("currency", "€")

    table = Table(title="Balance Summary", show_header=False, box=None, padding=(0, 2))
    table.add_column("Description", style="white")
    table.add_column("Value", justify="right")

    table.add_row("Total Income:", f"[green]{total_income:.2f} {currency_symbol}[/green]")
    table.add_row("Total Expenses:", f"[red]-{total_expenses:.2f} {currency_symbol}[/red]")
    table.add_row(Rule(style="white"), Rule(style="white"))
    balance_style = "green" if balance >= 0 else "red"
    table.add_row("[bold]Final Balance:[/bold]", f"[bold {balance_style}]{balance:.2f} {currency_symbol}[/bold {balance_style}]")

    console.print(Align.center(table))
    console.print(Rule(style="white"))

# Save Data
def save_data():
    """Saves the current finance_data to the JSON file."""
    with open('DATA.json', 'w') as f:
        json.dump(finance_data, f, indent=4)

# Add Transaction
def add_transaction(transaction_type: str):
    """Handles the logic for adding a new transaction (income or expense)."""
    color = "green" if transaction_type == "income" else "red"
    console.print(Rule(f"[bold {color}]Add New {transaction_type.capitalize()}[/bold {color}]", style=color))

    description = console.input("   [white]Description: [/white]")

    while True:
        try:
            amount_str = console.input("   [white]Amount: [/white]")
            amount = round(float(amount_str), 2)
            if amount <= 0:
                print("[red]   Amount must be a positive number.[/red]")
                continue
            break
        except ValueError:
            print("[red]   Invalid amount. Please enter a number (e.g., 50.25).[/red]")

    today_str = datetime.now().strftime('%Y-%m-%d')
    date_str = console.input(f"   [white]Date [default: {today_str}]: [/white]")
    if not date_str:
        date_str = today_str

    new_transaction = {"type": transaction_type, "amount": amount, "description": description, "date": date_str}
    finance_data["transactions"].append(new_transaction)
    finance_data["transactions"].sort(key=lambda x: x['date'], reverse=True)
    save_data()

    success_message = f"[bold {color}]New {transaction_type} added successfully![/bold {color}]"
    console.print(Rule(success_message, style=color))
    print()

# Change Currency
def change_currency():
    """Allows the user to change the currency symbol."""
    console.print(Rule("[bold cyan]Change Currency[/bold cyan]", style="cyan"))
    
    currencies = {"1": "€", "2": "$", "3": "¥"}
    
    console.print("   [white]Select a new currency:[/white]")
    console.print("   [yellow]1:[/yellow] Euro (€)")
    console.print("   [yellow]2:[/yellow] Dollar ($)")
    console.print("   [yellow]3:[/yellow] Yen (¥)")
    
    while True:
        choice = console.input("   [white]Choice (1-3): [/white]")
        if choice in currencies:
            new_currency = currencies[choice]
            finance_data["currency"] = new_currency
            save_data()
            console.print(Rule(f"[bold cyan]Currency changed to {new_currency}[/bold cyan]", style="cyan"))
            print()
            break
        else:
            console.print("[red]   Invalid choice. Please select 1, 2, or 3.[/red]")

# Command Loop
def command_loop():
    """The main loop that waits for user commands and executes the corresponding functions."""
    while True:
        user_input = console.input("[blue]Command >[/blue] ").lower()

        if user_input == "add income":
            add_transaction("income")

        elif user_input == "add expense":
            add_transaction("expense")

        elif user_input == "view balance":
            view_balance()

        elif user_input == "view all transactions":
            view_transactions()

        elif user_input == "change currency":
            change_currency()

        elif user_input == "exit":
            exit()

        else:
            print("[red]Unknown command[/red]")

# Main Function
load_data()
introduction()