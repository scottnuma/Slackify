import logging
import os

from dotenv import load_dotenv

load_dotenv()


class Settings(object):
    ENVIRONMENT: str = os.environ["FLASK_ENV"]

    SPOTIPY_CLIENT_ID: str = os.environ["SPOTIPY_CLIENT_ID"]
    SPOTIPY_CLIENT_SECRET: str = os.environ["SPOTIPY_CLIENT_SECRET"]
    SPOTIPY_REDIRECT_URI: str = os.environ["SPOTIPY_REDIRECT_URI"]

    VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE: str = os.environ[
        "VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE"
    ]
    GOOGLE_APPLICATION_CREDENTIALS: str = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
