from dotenv import load_dotenv
import os
import logging
import hvac

load_dotenv()

client = hvac.Client(url=os.environ["VAULT_ADDR"])
client.token = os.environ["VAULT_TOKEN"]
assert client.is_authenticated()

production_url = os.environ["PRODUCTION_URL"]
development_url = "http://localhost:5000"


class Config(object):
    """Base configuration"""

    ENVIRONMENT = os.getenv("FLASK_ENV", "production")

    _flask_secrets = client.secrets.kv.v1.read_secret(
        mount_point="slackify", path="flask"
    )["data"]
    FLASK_SESSION_KEY = _flask_secrets["FLASK_SESSION_KEY"]

    BASE_URL = os.getenv(
        "SLACKIFY_BASE_URL",
        development_url if ENVIRONMENT == "development" else production_url,
    )

    _slack_secrets = client.secrets.kv.v1.read_secret(
        mount_point="slackify", path="slack"
    )["data"]

    SLACK_VERIFICATION_TOKEN = _slack_secrets["SLACK_VERIFICATION_TOKEN"]
    SLACK_BOT_TOKEN = _slack_secrets["SLACK_BOT_TOKEN"]
    SLACK_SIGNING_SECRET = _slack_secrets["SLACK_SIGNING_SECRET"]
    SLACK_ID_KEY = _slack_secrets["SLACK_ID_KEY"]

    _spotify_secrets = client.secrets.kv.v1.read_secret(
        mount_point="slackify", path="spotify"
    )["data"]

    SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
    SPOTIPY_CLIENT_SECRET = _spotify_secrets["SPOTIPY_CLIENT_SECRET"]
    SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
