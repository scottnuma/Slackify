import logging

from spotipy import Spotify

logger = logging.getLogger(__name__)


def get_username(sp: Spotify):
    """Get the username from a login"""
    logger.info("authenticated Spotify")
    current_user_info = sp.current_user()
    username = current_user_info["id"]
    logger.info("got username: %s", username)
    return username


def get_playlists(sp: Spotify, username):
    """Get a list of playlist (name, id)"""
    playlists = sp.user_playlists(username, limit=10)["items"]
    formatted_playlists = [(playlist["id"], playlist["name"]) for playlist in playlists]
    logger.info("%s playlists: %s", username, formatted_playlists)
    return formatted_playlists
