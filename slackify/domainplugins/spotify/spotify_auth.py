import logging
import os
import sqlite3

import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util

from slackify.settings import Config

SCOPE = "playlist-modify-public"

logger = logging.getLogger(__name__)


def create_spotify_oauth(id):
    client_id = Config.SPOTIPY_CLIENT_ID
    client_secret = Config.SPOTIPY_CLIENT_SECRET
    redirect_uri = Config.SPOTIPY_REDIRECT_URI

    cache_dir = "_gen/caches"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_path = "{}/cache-{}".format(cache_dir, id)

    spotify_oauth = oauth2.SpotifyOAuth(
        client_id, client_secret, redirect_uri, scope=SCOPE, cache_path=cache_path
    )
    return spotify_oauth
