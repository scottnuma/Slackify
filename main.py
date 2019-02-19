import hashlib
import logging
import os
import queue
import threading

from flask import Flask, Response, jsonify
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter

import handler_app_mention
import handler_link_shared
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

sc = SlackClient(SLACK_BOT_TOKEN)

q = queue.Queue()


def process_queue(q):
    """Clear tasks from the queue.

    Verifies events, identifies the sender, and passes to handle_event.
    """
    logging.debug("starting thread %s", threading.currentThread().getName())

    while True:
        event = q.get()

        if SLACK_VERIFICATION_TOKEN != event.get('token'):
            logger.warning("event failed verification")
            q.task_done()
            continue

        slack_event = event['event']
        channel_id = generate_id(event['team_id'], slack_event['channel'])
        handle_event(slack_event, channel_id)
        q.task_done()


def generate_id(team_id, channel):
    """Create an id unique to each channel regardless of workspace."""
    combined = "github.com/scottnuma" + str(team_id) + str(channel)
    return hashlib.sha224(combined.encode("utf-8")).digest()


app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/api/v1/music", app)


@app.route('/healthcheck')
def healthy():
    """Provide quick affirmation of that the server is online"""
    logger.info("healthcheck ping")
    return 'ok'


@app.errorhandler(500)
def server_error(e):
    logger.error('An error occurred during a request.')
    return 'An internal error occurred.', 500


def handle_event(slack_event, channel_id):
    """Handle event with respective handler."""
    event_type = slack_event['type']
    if event_type == "app_mention":
        handler_app_mention.handle_app_mention(sc, slack_event, channel_id)
    elif event_type == "link_shared":
        handler_link_shared.link_handler(sc, slack_event, channel_id)
    else:
        logger.warning("Unhandled %s event: %s", event_type, slack_event)


@slack_events_adapter.on("app_mention")
def handle_app_mention(event):
    """Give friendly response in thread when @mentioned."""
    logger.info("received mention: %s", event)
    q.put(event)
    logger.info("sending 200")
    return Response(), 200


@slack_events_adapter.on("link_shared")
def slack_music_link_handler(event):
    """Pass link events to their respective handlers and respond."""
    logger.info("received event: %s", event)
    q.put(event)
    logger.info("sending 200")
    return Response(), 200


if __name__ == "__main__":
    logger.info("starting web server")

    threads_num = 3
    for i in range(threads_num):
        t = threading.Thread(name="Consumer-"+str(i),
                             target=process_queue, args=(q,))
        t.start()

    app.run(port=5000, host='0.0.0.0', debug=True)
