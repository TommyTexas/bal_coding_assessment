import sqlite3

conn = sqlite3.connect("mock.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")
cur.execute("""
DROP TABLE IF EXISTS keywords
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS keywords (
    keyword TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    occurrences INTEGER NOT NULL,
    last_used_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (keyword, user_id)
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    message TEXT,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()
