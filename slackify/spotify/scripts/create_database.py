import sqlite3
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = "/".join([CURR_DIR, "schema.sql"])
DB_FILE = "spotify.db"

conn = sqlite3.connect(DB_FILE)
with open(SCHEMA_FILE) as schema_file:
    conn.executescript(schema_file.read())
conn.close()
