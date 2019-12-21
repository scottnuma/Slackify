from typing import Dict

from celery.utils.log import get_task_logger
from slack import WebClient

from ensemble.plugins.plugin import Plugin

logger = get_task_logger(__name__)


class HelpMention(Plugin):
    @staticmethod
    def matches(event) -> bool:
        text = event["text"]

        if "spotify" in text and "help" in text:
            return True

    @staticmethod
    def handle(web_client: WebClient, channel_id: str, event: Dict):
        logger.info("responding to Spotify help")
        web_client.chat_postMessage(
            channel=event["channel"], text="these are the temporary help instructions."
        )
