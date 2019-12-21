import logging
import os

import spotipy.oauth2 as oauth2

from ensemble.plugins.spotify.config import SpotifyConfig

SCOPE = "playlist-modify-public"

logger = logging.getLogger(__name__)


def create_spotify_oauth(id):
    client_id = SpotifyConfig.SPOTIPY_CLIENT_ID
    client_secret = SpotifyConfig.SPOTIPY_CLIENT_SECRET
    redirect_uri = SpotifyConfig.SPOTIPY_REDIRECT_URI

    cache_dir = "_gen/caches"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_path = f"{cache_dir}/cache-{id}"

    spotify_oauth = oauth2.SpotifyOAuth(
        client_id, client_secret, redirect_uri, scope=SCOPE, cache_path=cache_path
    )
    return spotify_oauth
