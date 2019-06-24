import logging
import sqlite3

from flask import current_app

DATABASE = "spotify.db"

logger = logging.getLogger(__name__)


def get_db():
    logger.info("opening database connection")
    return sqlite3.connect(DATABASE)


def store_access_token(conn, spotify_user_id, access_token):
    """Stores an retrievable access token"""
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO user_auth (spotify_user_id, token) VALUES(?,?)""",
            (spotify_user_id, access_token),
        )
    except sqlite3.IntegrityError:
        cur.execute(
            """ UPDATE user_auth SET token = ? WHERE spotify_user_id = ?""",
            (access_token, spotify_user_id),
        )
    conn.commit()
    return cur.lastrowid


def get_access_token(conn, spotify_user_id):
    """
    Retrieve the access token for a Spotify user

    Returns None upon failure.
    """
    logger.info("retrieving access token for %s", spotify_user_id)
    cur = conn.cursor()
    query = "SELECT token FROM user_auth WHERE spotify_user_id=?"
    cur.execute(query, (spotify_user_id,))

    rows = cur.fetchall()

    # When no matches are found
    if len(rows) == 0:
        logger.info("Found no tokens for id")
        return None

    token = rows[0][0]
    return token


def get_playlist_user(conn, channel_id):
    """Get (playlist id, spotify user id) for a channel"""
    cur = conn.cursor()
    cur.execute(
        "SELECT playlist_id, spotify_user_id FROM playlist_info WHERE channel_id=?",
        (channel_id,),
    )
    rows = cur.fetchall()

    if len(rows) == 0:
        logger.info("Found no tokens for id")
        return None

    return rows[0]


def store_user_id(conn, channel_id, spotify_user_id):
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO playlist_info (channel_id, spotify_user_id) VALUES (?,?)""",
            (channel_id, spotify_user_id),
        )
    except sqlite3.IntegrityError:
        cur.execute(
            """ UPDATE playlist_info SET spotify_user_id = ? WHERE channel_id = ?""",
            (spotify_user_id, channel_id),
        )
    conn.commit()


def store_playlist_id(conn, channel_id, playlist_id):
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO playlist_info (channel_id, playlist_id) VALUES (?,?)""",
            (channel_id, playlist_id),
        )
    except sqlite3.IntegrityError:
        cur.execute(
            """ UPDATE playlist_info SET playlist_id = ? WHERE channel_id = ?""",
            (playlist_id, channel_id),
        )
    conn.commit()
