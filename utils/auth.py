# utils/auth.py
import sqlite3
from passlib.hash import bcrypt
from pathlib import Path

DB = Path("users.db")

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT
    )""")
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, bcrypt.hash(password)))
    conn.commit(); conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone(); conn.close()
    if not row: return False
    return bcrypt.verify(password, row[0])
