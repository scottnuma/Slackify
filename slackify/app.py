import queue
from typing import Dict
from typing import List
from typing import Tuple

from flask import Flask
from flask import Response
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from slackify.domainplugins import domain_plugins
from slackify.handlers import handle_app_mention
from slackify.handlers import handle_link
from slackify.oauth import oauth
from slackify.settings import Config
from slackify.util import generate_channel_id
from slackify.views import basics


def create_app():
    app = Flask(__name__)
    app.register_blueprint(basics)
    app.register_blueprint(oauth)

    for domain_plugin in domain_plugins:
        app.register_blueprint(
            domain_plugin.blueprint, url_prefix=domain_plugin.url_prefix
        )

    # app.register_blueprint(spotify_views.spotify_routes, url_prefix="/spotify")
    app.secret_key = Config.FLASK_SESSION_KEY

    slack_events_adapter = SlackEventAdapter(
        Config.SLACK_SIGNING_SECRET, "/api/v1/music", app,
    )
    web_client = WebClient(token=Config.SLACK_BOT_USER_OAUTH_ACCESS_TOKEN)
    slack_events_adapter.on("app_mention", on_mention(app, web_client))
    slack_events_adapter.on("link_shared", on_link_shared(app, web_client))

    return app


def on_mention(app: Flask, web_client: WebClient):
    def on_app_mention(event_data):
        """
        Give friendly response in thread when @mentioned.

        Slack API: https://api.slack.com/events/app_mention
        """
        event, channel_id = parse_event_and_id(event_data)

        app.logger.debug("received mention: %s", event)
        handle_app_mention(web_client, event, channel_id)
        app.logger.debug("sending 200")
        return Response(), 200

    return on_app_mention


def on_link_shared(app: Flask, web_client: WebClient):
    def slack_music_link_handler(event_data):
        """Pass link events to their respective handlers and respond."""
        event, channel_id = parse_event_and_id(event_data)
        app.logger.debug("received event: %s", event)
        handle_link(web_client, event, channel_id)
        app.logger.debug("sending 200")
        return Response(), 200

    return slack_music_link_handler


def parse_event_and_id(event_data: Dict) -> Tuple[Dict, str]:
    event = event_data["event"]
    team_id = event_data["team_id"]
    channel = event["channel"]
    channel_id = generate_channel_id(team_id, channel)
    return event, channel_id
