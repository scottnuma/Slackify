import logging
from typing import Dict

from slack import WebClient

from ensemble.plugins.plugin import Plugin

logger = logging.getLogger(__name__)


class ExampleMentionPlugin(Plugin):
    @staticmethod
    def matches(event) -> bool:
        return True

    @staticmethod
    def handle(web_client: WebClient, channel_id: str, event: Dict):
        web_client.chat_postMessage(channel=event["channel"], text="hi")


class ExampleLinkPlugin(Plugin):
    @staticmethod
    def matches(event: str) -> bool:
        return True

    @staticmethod
    def handle(web_client: WebClient, channel_id: str, event: Dict):
        web_client.reactions_add(
            channel=event["channel"], name="+1", timestamp=event["message_ts"],
        )
