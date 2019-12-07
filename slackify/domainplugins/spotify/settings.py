import logging
import os

from dotenv import load_dotenv

load_dotenv()


class Settings(object):
    SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
    SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
    SPOTIPY_REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']

    VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE = os.environ[
        'VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE'
    ]
    GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
