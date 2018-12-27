import logging
import re

import spotipy
import spotipy.util as util
from flask import Flask, Response, jsonify, request

playlist_maintainer_username = "newmascot"
playlist_id = "1UYhAHMEC42azRALlCCyn6"

# create logger with 'spam_application'
logger = logging.getLogger('slack_spotify_playlist')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('slack_spotify_playlist.log')
fh.setLevel(logging.DEBUG)

# create console handle
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


app = Flask(__name__)

token = util.prompt_for_user_token(
    "newmascot",
    "playlist-modify-public",
)
sp = spotipy.Spotify(token)
logger.info("Initialized and authenticated Spotipy")


@app.route('/healthcheck')
def healthy():
    logger.debug("healthcheck ping")
    return 'ok'


@app.route('/api/v0/music', methods=['POST'])
def music():
    user_id = request.form.get('user_id', '')
    if user_id == "USLACKBOT":
        logger.debug("Ignoring slackbot response")
        return Response(), 200

    text = request.form.get('text', '')
    track_ids = find_ids(text)
    logger.info("received message from channel")
    logger.info("identified these track ids: %s", track_ids)

    if track_ids:
        try:
            sp.user_playlist_add_tracks(
                playlist_maintainer_username, playlist_id, track_ids)
        except spotipy.client.SpotifyException:
            logger.error("failed to add track(s) to playlist: %s", track_ids)
            return jsonify(
                text="Hmm I wasn't able to add that track to the playlist",
            )
        else:
            logger.info(
                "successfully added track(s) to playlist: %s", track_ids)
            return Response(), 200

    return Response(), 200


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logger.error('An error occurred during a request.')
    return 'An internal error occurred.', 500


def find_ids(msg):
    """find_ids pulls the id of a track from its URL."""
    result = re.search(r"https://open\.spotify\.com/track/(\w+)[?]", msg)
    if not result:
        return []
    return result.groups()


if __name__ == "__main__":

    logger.info("Starting server")
    app.run(port=5000, host='0.0.0.0', debug=False, use_reloader=False)
