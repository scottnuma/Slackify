from dotenv import load_dotenv
import os
import logging
import hvac

load_dotenv()


production_url = os.environ["PRODUCTION_URL"]
development_url = "http://localhost:5000"


class Config(object):
    """Base configuration"""

    ENVIRONMENT = os.getenv("FLASK_ENV", "production")

    logging.info("using %s env", ENVIRONMENT)

    FLASK_SESSION_KEY = ""

    BASE_URL = os.getenv(
        "SLACKIFY_BASE_URL",
        development_url if ENVIRONMENT == "development" else production_url,
    )

    SLACK_VERIFICATION_TOKEN = ""
    SLACK_BOT_TOKEN = ""
    SLACK_SIGNING_SECRET = ""
    SLACK_ID_KEY = ""

    SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
    SPOTIPY_CLIENT_SECRET
    SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]

    VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE = os.environ[
        "VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE"
    ]
    GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
