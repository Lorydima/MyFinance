"""Shared configuration, paths, and visual constants for MyFinance."""

from __future__ import annotations

import sys
from pathlib import Path


def get_app_dir() -> Path:
    """Return the directory that stores the app data files.

    When the app is frozen into an executable, the files live next to the
    executable. During source execution, they live in the ``Src/`` directory.
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


APP_DIR = get_app_dir()
DATA_FILE = APP_DIR / "DATA.json"
ICON_FILE = APP_DIR / "MyFinance_Logo.ico"
LICENSE_FILE = APP_DIR / "LICENSE.txt"

VERSION = "3.0"
DATE_DEV = "06/06/2026"

FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 12, "bold")

COLOR_GREEN = "#27ae60"
COLOR_BG = "#4d4d4d"
