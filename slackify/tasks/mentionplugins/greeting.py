from typing import Dict

from slack import WebClient

from slackify.tasks.mentionplugins.plugin import MentionPlugin


class GreetingPlugin(MentionPlugin):
    @staticmethod
    def matches(text):
        return "hi" in text or "help" in text

    def handle(self, channel_id: str, event: Dict) -> None:
        response = ":notes: hi <@{}> - you can ask me to `link` or `unlink` this channel.".format(
            event["user"]
        )
        self.slack_client.chat_postMessage(
            channel=event["channel"], text=response, thread_ts=event["event_ts"],
        )
