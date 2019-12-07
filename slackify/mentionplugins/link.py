import logging

from plugin import MentionPlugin

from slackify import Config

logger = logging.getLogger(__name__)


class LinkPlugin(MentionPlugin):
    @staticmethod
    def matches(text):
        return "link" in text

    def handle(self, slack_client, channel_id, message) -> None:
        logger.info(
            "responding to %s for linking channel %s", message["user"], channel_id
        )
        token = spotify.database.generate_token(spotify.database.get_db(), channel_id)
        link = "/".join([Config.BASE_URL, "spotify/link", channel_id, token])
        response = f"Follow this link to link this channel: {link}"

        slack_client.api_call(
            "chat.postEphemeral",
            channel=message["channel"],
            text=response,
            user=message["user"],
        )
        slack_client.api_call(
            "reactions.add",
            channel=message["channel"],
            name="notes",
            timestamp=message["event_ts"],
        )
        return
