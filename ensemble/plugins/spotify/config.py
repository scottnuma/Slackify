import os

from dotenv import load_dotenv

load_dotenv()


class SpotifyConfig(object):
    SPOTIPY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    SPOTIPY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
    SPOTIPY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
