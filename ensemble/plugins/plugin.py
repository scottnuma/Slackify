from typing import Dict

from slack import WebClient


class Plugin(object):
    @staticmethod
    def matches(event: Dict) -> bool:
        raise NotImplementedError

    def handle(self, web_client: WebClient, channel_id: str, event: Dict) -> None:
        raise NotImplementedError
