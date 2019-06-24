import sqlite3

DB_FILE = "spotify.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("""CREATE TABLE playlist_info (
    channel_id TEXT PRIMARY KEY,
    playlist_id TEXT,
    spotify_user_id TEXT
    );"""
            )

cur.execute("""CREATE TABLE user_auth (
    spotifwy_user_id TEXT PRIMARY KEY,
    token TEXT NOT NULL
    );"""
            )
conn.commit()
conn.close()
