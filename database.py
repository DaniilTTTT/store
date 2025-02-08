import sqlite3

def get_db():
    conn = sqlite3.connect('users.db')
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name STRING 
                   )
                    """)

    conn.commit()
 
init_db()