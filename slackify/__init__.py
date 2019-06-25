import logging
import queue
import threading

from flask import Flask, Response, jsonify
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter

from .util import *
from .views import *
from .handlers import handle_app_mention, link_handler
from .spotify import spotify_views
from .settings import Config


logger = init_logger()


def process_queue(sc, q):
    """Clear tasks from the queue.

    Verifies events, identifies the sender, and passes to handle_event.
    """
    logger.debug("starting thread %s", threading.currentThread().getName())

    while True:
        event = q.get()

        if Config.SLACK_VERIFICATION_TOKEN != event.get("token"):
            logger.warning("event failed verification")
            q.task_done()
            continue

        slack_event = event["event"]
        id = generate_id(event["team_id"], slack_event["channel"])
        handle_event(sc, slack_event, id)
        q.task_done()


def handle_event(sc, slack_event, id):
    """Handle event with respective handler."""
    event_type = slack_event["type"]
    if event_type == "app_mention":
        handle_app_mention(sc, slack_event, id)
    elif event_type == "link_shared":
        link_handler(sc, slack_event, id)
    else:
        logger.warning("Unhandled %s event: %s", event_type, slack_event)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(basics)
    app.register_blueprint(spotify_views.spotify_routes, url_prefix="/spotify")
    app.secret_key = Config.FLASK_SESSION_KEY

    sc = SlackClient(Config.SLACK_BOT_TOKEN)

    q = queue.Queue()

    threads_num = 3
    for i in range(threads_num):
        t = threading.Thread(
            name="Consumer-" + str(i), target=process_queue, args=(sc, q)
        )
        t.start()

    slack_events_adapter = SlackEventAdapter(
        Config.SLACK_SIGNING_SECRET, "/api/v1/music", app
    )

    @slack_events_adapter.on("app_mention")
    def on_app_mention(event):
        """Give friendly response in thread when @mentioned."""
        app.logger.info("received mention: %s", event)
        q.put(event)
        app.logger.info("sending 200")
        return Response(), 200

    @slack_events_adapter.on("link_shared")
    def slack_music_link_handler(event):
        """Pass link events to their respective handlers and respond."""
        app.logger.info("received event: %s", event)
        q.put(event)
        app.logger.info("sending 200")
        return Response(), 200

    return app
