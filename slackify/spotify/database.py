import logging
import sqlite3
import secrets
import datetime
import json
import os
import base64

from google.cloud import firestore
from google.cloud import exceptions
from google.auth.exceptions import DefaultCredentialsError

from ..settings import Config, get_vault_client

logger = logging.getLogger(__name__)

TOKEN_COLLECTION = "tokens"
PLAYLIST_COLLECTION = "playlist_links"
USER_COLLECTION = "user_auth"


def get_db(env=Config.ENVIRONMENT):
    logger.info("opening database connection")
    return _get_db_client().collection("environment").document(env)


def _generate_new_key(lease_period):

    client = get_vault_client()
    cred_dict = client.secrets.gcp.generate_service_account_key(
        roleset="firestore-editor", method="GET"
    )

    if Config.ENVIRONMENT == "development":
        logger.info("shortening lease")
        # Reduce lease
        client.sys.renew_lease(lease_id=cred_dict["lease_id"], increment=lease_period)
    with open(Config.VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE, "w") as lease_file:
        lease_file.write(cred_dict["lease_id"])

    encoded_key = cred_dict["data"]["private_key_data"]
    key_str = base64.standard_b64decode(encoded_key).decode("utf-8")

    with open(Config.GOOGLE_APPLICATION_CREDENTIALS, "w") as cred_file:
        cred_file.write(key_str)


def _get_db_client():
    try:
        return firestore.Client()
    except DefaultCredentialsError:
        logger.info("failed to authenticate")

        if Config.ENVIRONMENT == "development":
            lease_period = 60 * 60
        else:
            lease_period = 31 * 24 * 60 * 60

        try:
            cred_file = open(Config.GOOGLE_APPLICATION_CREDENTIALS, "r")
        except FileNotFoundError:
            logger.info("failed to find default credentials file")
            _generate_new_key(lease_period)
        else:
            # Renew the current key
            logger.info("found default credentials file")

            with open(
                Config.VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE, "r"
            ) as lease_file:
                logger.info("found lease id")
                lease_id = lease_file.read()

            client = get_vault_client()
            result = client.sys.renew_lease(lease_id=lease_id, increment=lease_period)
            logger.info("renewed credential lease: %s", result)
            cred_file.close()
    return firestore.Client()


def store_access_token(conn, spotify_user_id, access_token):
    """Stores an retrievable access token"""
    return (
        conn.collection(USER_COLLECTION)
        .document(spotify_user_id)
        .set({"access_token": access_token})
    )


def get_access_token(conn, spotify_user_id):
    """
    Retrieve the access token for a Spotify user

    Returns None upon failure.
    """
    logger.info("retrieving access token for %s", spotify_user_id)
    doc_ref = conn.collection(USER_COLLECTION).document(spotify_user_id)
    try:
        doc = doc_ref.get()
    except exceptions.NotFound:
        logger.info("Found no tokens for id")
        return None
    if not doc.exists:
        return None
    return doc.to_dict()["access_token"]


def contains_channel(conn, channel_id):
    """Return if a channel is in the database"""
    doc = conn.collection(PLAYLIST_COLLECTION).document(channel_id).get()
    return doc.exists


def get_playlist_user(conn, channel_id):
    """Get (playlist id, spotify user id) for a channel"""
    doc = conn.collection(PLAYLIST_COLLECTION).document(channel_id).get()

    if not doc.exists:
        return None

    doc_dict = doc.to_dict()
    return (doc_dict["playlist_id"], doc_dict["spotify_user_id"])


def store_user_id(conn, channel_id, spotify_user_id):
    conn.collection(PLAYLIST_COLLECTION).document(channel_id).update(
        {"spotify_user_id": spotify_user_id}
    )


def store_playlist_id(conn, channel_id, playlist_id):
    conn.collection(PLAYLIST_COLLECTION).document(channel_id).set(
        {"channel_id": channel_id, "playlist_id": playlist_id}
    )


def delete_channel(conn, channel_id):
    """
    Removes the link between a channel and playlist and user

    Removes user's authentication token if there are no more associated channels.
    """
    conn.collection(PLAYLIST_COLLECTION).document(channel_id).delete()
    tokens = (
        conn.collection(TOKEN_COLLECTION).where("channel_id", "==", channel_id).stream()
    )

    for token in tokens:
        token.reference.delete()


def generate_token(conn, channel_id):
    """Generates and saves a one time token"""
    token = secrets.token_hex()
    conn.collection(TOKEN_COLLECTION).document().set(
        {
            "channel_id": channel_id,
            "token": token,
            "timestamp": firestore.SERVER_TIMESTAMP,
        }
    )
    return token


def verify_token(conn, channel_id, token):
    """
    Returns whether a token is valid

    If the token is valid, removes the token from memory.
    """
    valid_period = datetime.timedelta(days=1)
    yesterday = datetime.datetime.now() - valid_period

    query = (
        conn.collection(TOKEN_COLLECTION)
        .where("channel_id", "==", channel_id)
        .where("token", "==", token)
        .where("timestamp", ">=", yesterday)
    )

    for doc in query.stream():
        doc.reference.delete()
        logger.info("verified token %s", token)
        return True

    logger.info(
        "failed to verify that token, %s, for channel, %s, came after %s",
        token,
        channel_id,
        yesterday,
    )
    return False
