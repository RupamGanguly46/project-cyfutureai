import sqlite3
from datetime import datetime

DB_FILE = "conversations.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_input TEXT,
            bot_response TEXT,
            sentiment TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_chat(user_input, bot_response, sentiment):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO chats (timestamp, user_input, bot_response, sentiment) VALUES (?, ?, ?, ?)",
              (datetime.now().isoformat(), user_input, bot_response, sentiment))
    conn.commit()
    conn.close()

# Call this once at startup (will not overwrite if already created)
init_db()
