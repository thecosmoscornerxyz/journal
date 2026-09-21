#!/usr/bin/env python3

import sqlite3
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Import Force Chart
import sys
sys.path.append("/opt/force_chart")
from telemetry import signal_link

# Rich Settings
console = Console()

# Directories
DB_DIR = "/opt/journal/databases"

# Databases
DB = os.path.join(DB_DIR, "journal.db")

#=================================================#
#  ____        _        _                         |
# |  _ \  __ _| |_ __ _| |__   __ _ ___  ___      |
# | | | |/ _` | __/ _` | '_ \ / _` / __|/ _ \     |
# | |_| | (_| | || (_| | |_) | (_| \__ \  __/     |
# |____/ \__,_|\__\__,_|_.__/ \__,_|___/\___|     |
#                                                 |
#  _____                 _   _                    |
# |  ___|   _ _ __   ___| |_(_) ___  _ __  ___    |
# | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|   |
# |  _|| |_| | | | | (__| |_| | (_) | | | \__ \   |
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/   |
#                                                 |
#=================================================#

# Create Database Function
def create_table():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            location TEXT,
            activity TEXT,
            description TEXT,
            comments TEXT
        )
        """
    )

    conn.commit()
    conn.close()

# Save to Database Function
def save_journal(location, activity, description, comments):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO journal (
            location,
            activity,
            description,
            comments
        )
        VALUES (?, ?, ?, ?)
        """,
        (location, activity, description, comments),
    )

    conn.commit()
    conn.close()

create_table()

# Main Loop
while True:
    print(r"""
     _                              _
    | | ___  _   _ _ __ _ __   __ _| |
 _  | |/ _ \| | | | '__| '_ \ / _` | |
| |_| | (_) | |_| | |  | | | | (_| | |
 \___/ \___/ \__,_|_|  |_| |_|\__,_|_|

    """)
    console.print(
        Panel("""
1. New Entry

[q] Quit
        """,
            expand=False
        )
    )

    choice = input("What Will It Be Sir? ")

    if choice == "q":
        break

    match choice:
        case "1":
            console.print(
                Panel("""
 _____         _                   _____       _
|_   _|__   __| | __ _ _   _ ___  | ____|_ __ | |_ _ __ _   _
  | |/ _ \ / _` |/ _` | | | / __| |  _| | '_ \| __| '__| | | |
  | | (_) | (_| | (_| | |_| \__ \ | |___| | | | |_| |  | |_| |
  |_|\___/ \__,_|\__,_|\__, |___/ |_____|_| |_|\__|_|   \__, |
                       |___/                            |___/
                """)
            )

            location = Prompt.ask("Location")
            activity = Prompt.ask("Activity")
            description = Prompt.ask("Description")
            comments = Prompt.ask("Comments")

            save_journal(location, activity, description, comments)

# Signal Link
signal_link("journal-cli.py", "journal.db")
