from typing import Dict

from slack import WebClient

from slackify.mentionplugins.plugin import MentionPlugin


class GreetingPlugin(MentionPlugin):
    @staticmethod
    def matches(text):
        return "hi" in text or "help" in text

    def handle(self, slack_client: WebClient, channel_id: str, event: Dict) -> None:
        response = ":notes: hi <@{}> - you can ask me to `link` or `unlink` this channel.".format(
            event["user"]
        )
        slack_client.chat_postMessage(
            channel=event["channel"], text=response, thread_ts=event["event_ts"],
        )
