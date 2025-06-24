# import sqlite3
# from datetime import datetime

# DB_FILE = "conversations.db"

# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS chats (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp TEXT,
#             user_input TEXT,
#             bot_response TEXT,
#             sentiment TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# def insert_chat(user_input, bot_response, sentiment):
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("INSERT INTO chats (timestamp, user_input, bot_response, sentiment) VALUES (?, ?, ?, ?)",
#               (datetime.now().isoformat(), user_input, bot_response, sentiment))
#     conn.commit()
#     conn.close()

# # Call this once at startup (will not overwrite if already created)
# init_db()

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
            text_sentiment TEXT,
            audio_sentiment TEXT,
            fused_sentiment TEXT,
            user_audio_path TEXT,
            tts_audio_path TEXT,
            response_time_ms INTEGER,
            session_id TEXT,
            intent TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_chat(user_input, bot_response, text_sentiment=None, audio_sentiment=None,
                fused_sentiment=None, user_audio_path=None, tts_audio_path=None,
                response_time_ms=None, session_id=None, intent=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO chats (timestamp, user_input, bot_response, text_sentiment, audio_sentiment,
                           fused_sentiment, user_audio_path, tts_audio_path, response_time_ms,
                           session_id, intent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        user_input,
        bot_response,
        text_sentiment,
        audio_sentiment,
        fused_sentiment,
        user_audio_path,
        tts_audio_path,
        response_time_ms,
        session_id,
        intent
    ))
    conn.commit()
    conn.close()

# Call once at startup
init_db()
