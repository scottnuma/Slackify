import logging
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base configuration"""

    ENVIRONMENT: str = os.environ["FLASK_ENV"]

    FLASK_SESSION_KEY: str = os.environ["FLASK_SESSION_KEY"]

    BASE_URL: str = os.environ["SLACKIFY_BASE_URL"]

    SLACK_APP_ID: str = os.environ["SLACK_APP_ID"]
    SLACK_CLIENT_ID: str = os.environ["SLACK_CLIENT_ID"]
    SLACK_CLIENT_SECRET: str = os.environ["SLACK_CLIENT_SECRET"]
    SLACK_SIGNING_SECRET: str = os.environ["SLACK_SIGNING_SECRET"]

    SLACK_OAUTH_ACCESS_TOKEN: str = os.environ["SLACK_OAUTH_ACCESS_TOKEN"]
    SLACK_BOT_USER_OAUTH_ACCESS_TOKEN: str = os.environ[
        "SLACK_BOT_USER_OAUTH_ACCESS_TOKEN"
    ]

    SLACK_ID_KEY: str = os.environ["SLACK_ID_KEY"]
