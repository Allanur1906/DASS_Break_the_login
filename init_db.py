import sqlite3
from datetime import datetime, UTC

conn = sqlite3.connect("database.db")
c = conn.cursor()
# USERS
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    locked INTEGER DEFAULT 0,
    created_at TEXT
)
""")
# Pasword reset
c.execute("""
CREATE TABLE IF NOT EXISTS reset_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    token TEXT,
    expires_at TEXT,
    used INTEGER DEFAULT 0
)
""")
# AUDIT LOGS
c.execute("""
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    action TEXT,
    timestamp TEXT,
    ip_address TEXT
)
""")
# Notes
c.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    owner_email TEXT,
    created_at TEXT
)
""")
def add_column(table, column, definition):
    columns = [row[1] for row in c.execute(f"PRAGMA table_info({table})")]
    if column not in columns:
        c.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

add_column("users", "created_at", "TEXT")
add_column("reset_tokens", "expires_at", "TEXT")
add_column("reset_tokens", "used", "INTEGER DEFAULT 0")
add_column("audit_logs", "ip_address", "TEXT")
add_column("notes", "created_at", "TEXT")
c.execute(
    "UPDATE users SET created_at=? WHERE created_at IS NULL",
    (datetime.now(UTC).isoformat(timespec="seconds"),)
)
c.execute(
    "UPDATE notes SET created_at=? WHERE created_at IS NULL",
    (datetime.now(UTC).isoformat(timespec="seconds"),)
)
conn.commit()
conn.close()
print("Database created successfully")
