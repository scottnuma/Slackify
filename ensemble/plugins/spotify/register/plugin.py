import logging
from typing import Dict

from flask import current_app
from slack import WebClient

from ensemble.config import Config
from ensemble.plugins.plugin import Plugin
from ensemble.plugins.spotify.database import get_spotify_db
from ensemble.plugins.spotify.register.database import generate_token

logger = logging.getLogger(__name__)


class RegisterMention(Plugin):
    @staticmethod
    def matches(event) -> bool:
        text = event["text"]

        if "spotify" in text and "register" in text:
            return True

    @staticmethod
    def handle(web_client: WebClient, channel_id: str, event: Dict):
        current_app.logger.info(
            "responding to %s for linking channel %s", event["user"], channel_id
        )
        token = generate_token(get_spotify_db(), channel_id)
        link = "/".join([Config.BASE_URL, "spotify/link", channel_id, token,])
        response = f"Follow this link to link this channel: {link}"

        web_client.api_call(
            "chat.postEphemeral",
            channel=event["channel"],
            text=response,
            user=event["user"],
        )
        web_client.api_call(
            "reactions.add",
            channel=event["channel"],
            name="notes",
            timestamp=event["event_ts"],
        )
        return


class UnregisterMention(Plugin):
    @staticmethod
    def matches(text):
        return "unregister" in text

    @staticmethod
    def handle(web_client: WebClient, channel_id: str, event: Dict) -> None:
        logger.info("responding to unlink request")
        token = generate_token(get_spotify_db(), channel_id)
        link = "/".join([Config.BASE_URL, "spotify/unlink", channel_id, token])
        response = "Follow this link to unlink this channel: {}".format(link)

        web_client.chat_postEphemeral(
            channel=event["channel"], text=response, user=event["user"],
        )
        web_client.chat_reactionsAdd(
            channel=event["channel"], name="notes", timestamp=event["event_ts"],
        )
        return
