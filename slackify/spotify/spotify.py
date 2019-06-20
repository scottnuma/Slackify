import logging
import re
import sqlite3

import spotipy
import spotipy.util as util
from flask import Flask, Response, jsonify, request

from .spotify_auth import retrieve_access_token, DB_FILE


logger = logging.getLogger(__name__)

playlist_maintainer_username = "newmascot"
playlist_id = "1UYhAHMEC42azRALlCCyn6"

SPOTIFY_AUTH_URL = "https://newma.localtunnel.me/spotify/auth/init/"
authentication_request_template = "link your Spotify account to this channel: {}{}"

ADD_SUCCESS = "success"


def find_ids(msg):
    """Pull the id of a track from its URL."""
    result = re.search(r"https://open\.spotify\.com/track/(\w+)", msg)
    if not result:
        return []
    return result.groups()


def handler(id, link):
    """
    Add the track in link to the playlist associated with id.

    Returns the response text if any.

    id: reference to a specific slack channel
    link: a dictionary from the Slack API
    """
    logger.info("handling link: %s", link)
    logger.info("received from: %s", id)
 
    authentication_request_msg = authentication_request_template.format(SPOTIFY_AUTH_URL,id)

    text = link.get('url')
    if not text:
        logger.info("no URL found")
        return

    track_ids = find_ids(text)
    logger.info("identified these track ids: %s", track_ids)

    if track_ids:
        try:
            logger.info("attempting Spotify authentication")
            conn = sqlite3.connect(DB_FILE)
            token = retrieve_access_token(conn, id)
            logger.info("current token: %s", token)
            conn.close()

            if token is None:
                logger.info("failed to retrieve access token")
                return authentication_request_msg

            sp = spotipy.Spotify(token)
            logger.info("authenticated Spotify")
            sp.user_playlist_add_tracks(
                playlist_maintainer_username, playlist_id, track_ids)
        except spotipy.client.SpotifyException as error:
            logger.error(
                "failed to add track(s) to playlist: %s due to %s", track_ids, error)
            if error.http_status == 401:
                return authentication_request_msg
            return "Hmm I wasn't able to add a track to the playlist"
        else:
            logger.info(
                "successfully added track(s) to playlist: %s", track_ids)
            return ADD_SUCCESS

    else:
        logger.info("did not identify any tracks in: %s", link)


# Ideally we'd be able to use different accounts depending on what
# channel and workspace they're in. This would require authentication
# through Slack, rather than just through terminal.

# SpotifyClients should be able to provide the proper Spotify client
# for each channel and workspace.
class SpotifyClients:
    def __init__(self):
        self.clients = dict()

    def get(self, id):
        if id not in self.clients:
            self.init(id)
        return self.clients[id]

    def init(self, id):
        token = util.prompt_for_user_token(
            "newmascot",
            "playlist-modify-public",
        )
        self.clients[id] = spotipy.Spotify(token)
