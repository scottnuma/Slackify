import logging
import re

import spotipy
import spotipy.util as util

from flask import Flask, Response, jsonify, request

logger = logging.getLogger(__name__)

playlist_maintainer_username = "newmascot"
playlist_id = "1UYhAHMEC42azRALlCCyn6"

token = util.prompt_for_user_token(
    "newmascot",
    "playlist-modify-public",
)

sp = spotipy.Spotify(token)
logger.info("authenticated Spotify")


def find_ids(msg):
    """find_ids pulls the id of a track from its URL."""
    result = re.search(r"https://open\.spotify\.com/track/(\w+)[?]", msg)
    if not result:
        return []
    return result.groups()


def handler(id, link):
    """handler adds the track in link to the playlist associated with id.

    id: reference to a specific slack channel
    link: a dictionary from the Slack API
    """
    logger.info("handling link: %s", link)

    text = link.get('url')
    if not text:
        logger.info("no URL found")
        return

    track_ids = find_ids(text)
    logger.info("identified these track ids: %s", track_ids)

    if track_ids:
        try:
            sp.user_playlist_add_tracks(
                playlist_maintainer_username, playlist_id, track_ids)
        except spotipy.client.SpotifyException:
            # logger.error("failed to add track(s) to playlist: %s", track_ids)
            return jsonify(
                text="Hmm I wasn't able to add that track to the playlist",
            )
        else:
            # logger.info(
                # "successfully added track(s) to playlist: %s", track_ids)
            pass
