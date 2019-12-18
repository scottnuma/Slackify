from flask import Blueprint
from plugin import DomainPlugin


class SpotifyPlugin(DomainPlugin):
    URL_prefix = "/spotify"
    blueprint = Blueprint("spotify", __name__)

    @staticmethod
    def matches(domain: str) -> bool:
        return domain == "open.spotify.com"

    def handle(self, id, link) -> str:
        return "pretended to handle Spotify link"
