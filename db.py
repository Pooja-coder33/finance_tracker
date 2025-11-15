import sqlite3
import pandas as pd
import streamlit as st

# Connect to database
conn = sqlite3.connect(
    r"C:\Users\Pooja\OneDrive\Documents\AsusProArtCalibration\OneDrive\Desktop\fm folder\finance_manager\finance.db",
    check_same_thread=False
)
cursor = conn.cursor()

# ------------------- INITIALIZE DATABASE -------------------
def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()

# ------------------- USER FUNCTIONS -------------------
def add_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing = cursor.fetchone()
    if existing:
        return "exists"
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    return "ok"

def login_user(username, password):
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        return user[0]
    return None

# ------------------- TRANSACTION FUNCTIONS -------------------
def add_transaction(user_id, date, category, amount, type_, description, notes):
    cursor.execute("""
        INSERT INTO transactions (user_id, date, category, amount, type, description, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, str(date), category, amount, type_, description, notes))
    conn.commit()

def fetch_data(user_id):
    cursor.execute("""
        SELECT id, date, category, amount, type, description, notes
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["id", "date", "category", "amount", "type", "description", "notes"])
    return df

