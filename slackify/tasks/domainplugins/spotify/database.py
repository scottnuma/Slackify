import base64
import datetime
import json
import logging
import os
import secrets
import sqlite3
from typing import Optional

from google.auth.exceptions import DefaultCredentialsError
from google.cloud import exceptions
from google.cloud.firestore import Client
from google.cloud.firestore import SERVER_TIMESTAMP
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1.types import WriteResult

from slackify.tasks.domainplugins.spotify.settings import Settings

logger = logging.getLogger(__name__)

TOKEN_COLLECTION = "tokens"
PLAYLIST_COLLECTION = "playlist_links"
USER_COLLECTION = "user_auth"


def get_db(env: str = Settings.ENVIRONMENT) -> DocumentReference:
    conn = _get_db_client()
    return conn.collection("environment").document(env)


def _get_db_client() -> Client:
    client = Client()
    logger.info("authenticated with found service account")
    return client


def store_access_token(
    conn: Client, spotify_user_id: str, access_token: str,
) -> WriteResult:
    """Stores an retrievable access token"""
    return (
        conn.collection(USER_COLLECTION)
        .document(spotify_user_id)
        .set({"access_token": access_token})
    )


def get_access_token(conn: Client, spotify_user_id: str) -> Optional[str]:
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


def contains_channel(conn: Client, channel_id: str) -> bool:
    """Return if a channel is in the database"""
    doc = conn.collection(PLAYLIST_COLLECTION).document(channel_id).get()
    return doc.exists


def get_playlist_user(conn: Client, channel_id: str) -> Tuple[str, str]:
    """
    Get (playlist id, spotify user id) for a channel

    Either playlist id or spotify user id may be None
    """
    doc = conn.collection(PLAYLIST_COLLECTION).document(channel_id).get()

    if not doc.exists:
        return None

    doc_dict = doc.to_dict()
    return (doc_dict.get("playlist_id"), doc_dict.get("spotify_user_id"))


def _upsert_playlist_collection(
    conn: Client, channel_id: str, data: Dict[str, str]
) -> WriteResult:
    doc_ref = conn.collection(PLAYLIST_COLLECTION).document(channel_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc_ref.update(data)
    else:
        return doc_ref.set(data)


def store_user_id(conn: Client, channel_id: str, spotify_user_id: str) -> WriteResult:
    data = {"spotify_user_id": spotify_user_id}
    return _upsert_playlist_collection(Client, channel_id, data)


def store_playlist_id(conn: Client, channel_id: str, playlist_id: str) -> WriteResult:
    """
    Store the playlist id of a channel

   Does not assume that a document already exists for the channel
    """
    data = {"playlist_id": playlist_id}
    return _upsert_playlist_collection(conn, channel_id, data)


def delete_channel(conn: Client, channel_id: str) -> None:
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


def generate_token(conn: Client, channel_id: str) -> str:
    """Generates and saves a one time token"""
    token = secrets.token_hex()
    conn.collection(TOKEN_COLLECTION).document().set(
        {"channel_id": channel_id, "token": token, "timestamp": SERVER_TIMESTAMP,}
    )
    return token


def verify_token(conn: Client, channel_id: str, token: str) -> bool:
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
