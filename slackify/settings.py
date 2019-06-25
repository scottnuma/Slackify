from dotenv import load_dotenv
import os
import logging

load_dotenv()


class Config(object):
    """Base configuration"""

    ENVIRONMENT = os.getenv("SLACK_MUSIC_ENVIRONMENT", "prod")

    SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    SLACK_ID_KEY = os.environ["SLACK_ID_KEY"]

    FLASK_SESSION_KEY = os.environ["FLASK_SESSION_KEY"]

    SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
    SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
    SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
