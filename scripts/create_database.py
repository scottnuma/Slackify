import sqlite3

DB_FILE = "tokens.db"

sql_query = """CREATE TABLE tokens (
 id BLOB PRIMARY KEY,
 token TEXT NOT NULL
);"""

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute(sql_query)