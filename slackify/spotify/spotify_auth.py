import os
import logging
import sqlite3

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

SCOPE="playlist-modify-public"

logger = logging.getLogger(__name__)

DB_FILE = "tokens.db"


def create_spotify_oauth(id):
    client_id = os.environ['SPOTIPY_CLIENT_ID']
    client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
    redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']

    cache_dir = "caches"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_path = "{}/cache-{}".format(cache_dir, id)
    
    spotify_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=SCOPE, cache_path=cache_path)
    return spotify_oauth

def store_access_token(conn, id, access_token):
    """Stores an retrievable access token"""
    cur = conn.cursor()
    sql_query = '''INSERT INTO tokens (id, token) VALUES(?,?)'''
    try:
        cur.execute(sql_query, (id, access_token))
    except sqlite3.IntegrityError:
        cur.execute(''' UPDATE tokens SET token = ? WHERE id = ?''', (access_token, id))
    conn.commit()
    return cur.lastrowid

def retrieve_access_token(conn, id):
    """
    Retrieve the access token for a specific Slack channel
    
    Returns None upon failure.
    """
    logger.info("retrieving access token for %s", id)
    cur = conn.cursor()
    query = "SELECT token FROM tokens WHERE id=?"
    cur.execute(query, (id,))
 
    rows = cur.fetchall()

    # When no matches are found
    if len(rows) == 0:
        logger.info("Found no tokens for id")
        return None

    token = rows[0][0]
    return token
