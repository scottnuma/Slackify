from typing import List

from flask import Blueprint

# from spotify_temp import SpotifyPlugin


class DomainPlugin(object):
    """Hanlde actions for a set of domains."""

    blueprint: Blueprint
    URL_prefix: str

    @staticmethod
    def matches(link: str) -> bool:
        """Return whether a link is handled by the Plugin."""
        raise NotImplementedError

    def handle(self, id, link) -> str:
        """
        Takes action upon a message

        Returns: feedback string for the end user.
        """
        raise NotImplementedError
