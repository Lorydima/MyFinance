"""Persistence helpers for MyFinance transaction data."""

from __future__ import annotations

import json
from datetime import datetime

from .config import DATA_FILE


def parse_date(date_str: str) -> datetime:
    """Parse a supported date format and return ``datetime.min`` on failure."""

    for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime.min


def default_finance_data() -> dict:
    """Return the default data structure used by the application."""

    return {"currency": "€", "transactions": []}


def save_data(finance_data: dict) -> None:
    """Write finance data to ``DATA.json`` next to the application files."""

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(finance_data, file, indent=4)


def load_data() -> dict:
    """Load finance data and migrate older records when needed."""

    if not DATA_FILE.exists():
        return default_finance_data()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return default_finance_data()

    if "currency" not in data:
        data["currency"] = "€"
    if "transactions" not in data:
        data["transactions"] = []

    migrated = False

    for transaction in data.get("transactions", []):
        # Older releases stored transaction types as enter/exit.
        if transaction.get("type") == "enter":
            transaction["type"] = "income"
            migrated = True
        elif transaction.get("type") == "exit":
            transaction["type"] = "expense"
            migrated = True

        # Normalize every date to the current short format used by the app.
        if "date" in transaction:
            dt = parse_date(transaction["date"])
            if dt != datetime.min:
                new_date = dt.strftime("%d/%m/%y")
                if transaction["date"] != new_date:
                    transaction["date"] = new_date
                    migrated = True

    if migrated:
        save_data(data)

    return data

