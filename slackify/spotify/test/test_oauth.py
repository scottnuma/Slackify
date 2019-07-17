import unittest
from unittest import mock

import slackify


class TestOAuth(unittest.TestCase):
    def test_create_spotify_oauth(self):
        self.assertIsNotNone(
            slackify.spotify.spotify_auth.create_spotify_oauth("test_id")
        )
