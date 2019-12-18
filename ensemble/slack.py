import logging
from typing import Dict
from typing import Tuple

from flask import current_app
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from ensemble.config import Config
from ensemble.plugins import mention_plugins
from ensemble.plugins.handlers import process_app_mention
from ensemble.plugins.handlers import process_link_shared

logger = logging.getLogger(__name__)


def register_slack(app: Flask):
    SLACK_ENDPOINT = "/api/v1/music"

    slack_event_adapter = SlackEventAdapter(
        Config.SLACK_SIGNING_SECRET, SLACK_ENDPOINT, app,
    )

    web_client = WebClient(token=Config.SLACK_BOT_USER_OAUTH_ACCESS_TOKEN)

    slack_event_adapter.on(
        "app_mention", create_handle_mention(web_client),
    )

    slack_event_adapter.on(
        "link_shared", create_handle_link_shared(web_client),
    )


def create_handle_mention(web_client: WebClient):
    def handle_mention(event_data: Dict):
        current_app.logger.info("received mention event: %s", event_data)
        process_app_mention(web_client, event_data)

    return handle_mention


def create_handle_link_shared(web_client: WebClient):
    def handle_link_shared(event_data: Dict):
        current_app.logger.info("received link shared event: %s", event_data)
        process_link_shared(web_client, event_data)

    return handle_link_shared
