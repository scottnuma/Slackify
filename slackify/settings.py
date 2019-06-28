from dotenv import load_dotenv
import os
import logging

load_dotenv()

production_url = "https://slackify.scottnumamoto.com"
development_url = "http://localhost:5000"


class Config(object):
    """Base configuration"""

    ENVIRONMENT = os.getenv("FLASK_ENV", "production")
    FLASK_SESSION_KEY = os.environ["FLASK_SESSION_KEY"]

    BASE_URL = os.getenv(
        "SLACKIFY_BASE_URL",
        development_url if ENVIRONMENT == "development" else production_url,
    )

    SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    SLACK_ID_KEY = os.environ["SLACK_ID_KEY"]

    SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
    SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
    SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
