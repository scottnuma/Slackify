import os
import logging

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

SCOPE="playlist-modify-public"

logger = logging.getLogger(__name__)


def create_spotify_oauth(username):
    client_id = os.environ['SPOTIPY_CLIENT_ID']
    client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
    redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']

    cache_dir = "caches"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_path = "{}/cache-{}".format(cache_dir, username)
    
    spotify_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=SCOPE, cache_path=cache_path)
    return spotify_oauth

def store_access_token(id, username, access_token):
    """Stores an retrievable access token"""
    logger.exception("store_access_token unimplemented")