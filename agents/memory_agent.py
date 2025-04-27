import sqlite3
from pathlib import Path

# Ensure the database directory exists
db_path = Path("data/memory.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

def log_session(summary_text):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create table if not exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS forecast_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert new session
    c.execute("INSERT INTO forecast_memory (summary) VALUES (?)", (summary_text,))
    
    conn.commit()
    conn.close()

def fetch_recent_sessions(limit=5):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("SELECT timestamp, summary FROM forecast_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    
    conn.close()
    return rows
