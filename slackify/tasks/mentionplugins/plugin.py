from typing import List
from typing import Optional


class MentionPlugin(object):
    def __init__(self, slack_client):
        self.slack_client = slack_client

    @staticmethod
    def matches(text: str) -> bool:
        raise NotImplementedError

    def handle(self, channel_id, message) -> None:
        raise NotImplementedError
