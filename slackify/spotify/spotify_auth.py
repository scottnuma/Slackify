import os
import logging
import sqlite3

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

SCOPE = "playlist-modify-public"

logger = logging.getLogger(__name__)


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
