from typing import List
from typing import Optional


class MentionPlugin(object):
    @staticmethod
    def matches(text: str) -> bool:
        raise NotImplementedError

    def handle(self, slack_client, channel_id, message) -> None:
        raise NotImplementedError
