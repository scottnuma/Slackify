import logging
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base configuration"""

    ENVIRONMENT = os.environ["FLASK_ENV"]
    logging.info("using %s env", ENVIRONMENT)

    FLASK_SESSION_KEY = os.environ["FLASK_SESSION_KEY"]

    BASE_URL = os.environ["SLACKIFY_BASE_URL"]

    SLACK_APP_ID = os.environ["SLACK_APP_ID"]
    SLACK_CLIENT_ID = os.environ["SLACK_CLIENT_ID"]
    SLACK_CLIENT_SECRET = os.environ["SLACK_CLIENT_SECRET"]
    SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

    SLACK_OAUTH_ACCESS_TOKEN = os.environ["SLACK_OAUTH_ACCESS_TOKEN"]
    SLACK_BOT_USER_OAUTH_ACCESS_TOKEN = os.environ["SLACK_BOT_USER_OAUTH_ACCESS_TOKEN"]

    SLACK_ID_KEY = os.environ["SLACK_ID_KEY"]
