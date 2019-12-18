import logging
import re

import spotipy

from .database import get_access_token
from .database import get_db
from .database import get_playlist_user
from slackify.settings import Config


logger = logging.getLogger(__name__)


SPOTIFY_AUTH_URL = f"https://{Config.BASE_URL}/spotify/auth/init/"
authentication_request_template = "Link your playlist to this channel: {}{}"
PLAYLIST_SELECT_URL = f"https://{Config.BASE_URL}/select_playlist/channel_id/"
playlist_selct_msg = "Please select the playlist to connect: {}{}"
ADD_SUCCESS = "success"


def handler(channel_id: str, link):
    """
    Add the track in link to the playlist associated with channel_id.

    Returns the response text if any.

    channel_id: reference to a specific slack channel
    link: a dictionary from the Slack API
    """
    logger.info("handling link: %s", link)
    logger.info("received from: %s", channel_id)

    authentication_request_msg = authentication_request_template.format(
        SPOTIFY_AUTH_URL, channel_id
    )

    text = link["url"]

    track_ids = find_ids(text)
    logger.info("identified these track ids: %s", track_ids)

    if not track_ids:
        logger.info("did not identify any tracks in: %s", link)
        return

    try:
        logger.info("attempting Spotify authentication")
        query = get_playlist_user(get_db(), channel_id)
        if query is None or query[0] is None:
            logger.info("channel is missing playlist or user")
            return authentication_request_msg

        playlist_id, user_id = query

        # If the playlist has not been selected
        if user_id is None:
            return playlist_selct_msg.format(PLAYLIST_SELECT_URL, channel_id)

        token = get_access_token(get_db(), user_id)
        if token is None:
            logger.info("user is missing token")
            return authentication_request_msg
        logger.info("current token: %s", token)

        sp = spotipy.Spotify(token)
        logger.info("authenticated Spotify")

        logger.info(
            "adding tracks (%s) to user (%s) playlist (%s)",
            track_ids,
            user_id,
            playlist_id,
        )
        sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)
    except spotipy.client.SpotifyException as error:
        logger.error(
            "failed to add track(s) to playlist: %s due to %s", track_ids, error
        )
        if error.http_status == 401:
            return authentication_request_msg
        return "Hmm I wasn't able to add a track to the playlist"
    else:
        logger.info("successfully added track(s) to playlist: %s", track_ids)
        return ADD_SUCCESS


def find_ids(msg: str):
    """Pull the id of a track from its URL."""
    result = re.search(r"https://open\.spotify\.com/track/(\w+)", msg)
    if not result:
        return []
    return result.groups()


def get_username(sp: spotipy.Spotify):
    """Get the username from a login"""
    logger.info("authenticated Spotify")
    current_user_info = sp.current_user()
    username = current_user_info["id"]
    logger.info("got username: %s", username)
    return username


def get_playlists(sp: spotipy.Spotify, username):
    """Get a list of playlist (name, id)"""
    playlists = sp.user_playlists(username, limit=10)["items"]
    formatted_playlists = [(playlist["id"], playlist["name"]) for playlist in playlists]
    logger.info("%s playlists: %s", username, formatted_playlists)
    return formatted_playlists
