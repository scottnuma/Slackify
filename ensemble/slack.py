import logging
from typing import Dict

from flask import current_app
from flask import Flask
from slackeventsapi import SlackEventAdapter

from ensemble.config import Config
from ensemble.plugins.handlers import process_app_mention
from ensemble.plugins.handlers import process_link_shared

logger = logging.getLogger(__name__)


def register_slack(app: Flask):
    SLACK_ENDPOINT = "/api/v1/music"

    slack_event_adapter = SlackEventAdapter(
        Config.SLACK_SIGNING_SECRET, SLACK_ENDPOINT, app,
    )

    slack_event_adapter.on(
        "app_mention", handle_mention,
    )
    slack_event_adapter.on(
        "link_shared", handle_link_shared,
    )


def handle_mention(event_data: Dict):
    current_app.logger.debug("received mention event: %s", event_data)
    process_app_mention.delay(event_data)


def handle_link_shared(event_data: Dict):
    current_app.logger.debug("received link shared event: %s", event_data)
    process_link_shared.delay(event_data)
