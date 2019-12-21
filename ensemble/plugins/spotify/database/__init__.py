import logging
from typing import Dict
from typing import Optional
from typing import Tuple

from google.cloud import exceptions
from google.cloud.firestore import Client
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1.types import WriteResult

from ensemble.database import get_db


logger = logging.getLogger(__name__)

TOKEN_COLLECTION = "tokens"
PLAYLIST_COLLECTION = "playlist_links"
USER_COLLECTION = "user_auth"
PLUGIN_NAME = "spotify"


def get_spotify_db() -> DocumentReference:
    """Return the documen that contains state for Spotify."""
    doc = get_db()
    return doc.document(PLUGIN_NAME)


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
