import logging
import os
import hashlib

from flask import Flask, Response, jsonify, request
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient

import spotify


def init_logger():
    """Initialize logger with labeling and locations."""
    # create logger with 'spam_application'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')

    # create file handler which logs even debug messages
    fh = logging.FileHandler('slack_spotify_playlist.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # create console handle
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = init_logger()

SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
if not SLACK_SIGNING_SECRET:
    logger.exception("SLACK_SIGNING_SECRET environment variable not found")

SLACK_VERIFICATION_TOKEN = os.environ.get("SLACK_VERIFICATION_TOKEN")
if not SLACK_VERIFICATION_TOKEN:
    logger.exception("SLACK_VERIFICATION_TOKEN environment variable not found")

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
if not SLACK_BOT_TOKEN:
    logger.exception("SLACK_BOT_TOKEN environment variable not found")

ENVIRONMENT = os.environ.get("SLACK_MUSIC_ENVIRONMENT") or "prod"

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/api/v1/music", app)

domain_handler = {'open.spotify.com': spotify.handler}

sc = SlackClient(SLACK_BOT_TOKEN)

def handle_link(id, links):
    """Pass each link to their service's handler."""
    handler_feedback = []

    if not links:
        logger.info("ignoring empty links")
        return

    if len(links) > 1:
        logger.info("multiple links given to handle_link")
    
    for link in links:
        domain = link.get('domain')
        if domain not in domain_handler:
            logger.info("ignoring unrecognized domain: %s", domain)
            continue

        logger.info("passing link to domain handler")
        handler_feedback.append(domain_handler[domain](id, link))
            
    return handler_feedback
            

def generate_id(team_id, channel):
    """Create an id unique to each channel regardless of workspace."""
    combined = "github.com/scottnuma" + str(team_id) + str(channel)
    return hashlib.sha224(combined.encode("utf-8")).digest()


@app.route('/healthcheck')
def healthy():
    logger.info("healthcheck ping")
    return 'ok'


@slack_events_adapter.on("link_shared")
def slack_music_link_handler(event):
    logger.info("received event: %s", event)
    if SLACK_VERIFICATION_TOKEN != event.get('token'):
        logger.warn("event failed verification")
        return 500

    slack_event = event.get('event')
    if not slack_event:
        logger.info("not a slack event")
        return 500

    id = generate_id(event.get('team_id'), slack_event.get('channel'))

    perfect_results = True
    for result in handle_link(id, slack_event.get('links')):
        if result != spotify.ADD_SUCCESS:
            perfect_results = False
            sc.api_call(
                "chat.postMessage",
                channel=slack_event.get('channel'),
                text=result,
                thread_ts=slack_event.get('message_ts')
            )

    if perfect_results:
        sc.api_call(
            "reactions.add",
            channel=slack_event.get('channel'),
            name="notes",
            timestamp=slack_event.get('message_ts')
        )
    
    return Response(), 200


@app.errorhandler(500)
def server_error(e):
    logger.error('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    logger.info("starting web server")
    app.run(port=5000, host='0.0.0.0', debug=True)
