import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "processing_history.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processing_history (
            process_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            total_records INTEGER,
            duplicate_records INTEGER,
            missing_values INTEGER,
            processing_status TEXT,
            processing_time TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_history(filename, total_records, duplicates, missing, status="completed"):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO processing_history (filename, total_records, duplicate_records, missing_values, processing_status, processing_time) VALUES (?, ?, ?, ?, ?, ?)",
        (filename, total_records, duplicates, missing, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()
