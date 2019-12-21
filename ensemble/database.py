"""
database contains the primitives for persistent state.
"""
import logging

from google.cloud.firestore import Client
from google.cloud.firestore_v1.document import DocumentReference

from ensemble.config import Config

logger = logging.getLogger(__name__)


def get_db(env: str = Config.ENVIRONMENT) -> DocumentReference:
    """Return the document that contains state for an environment."""
    conn = _get_db_client()
    return conn.collection("environment").document(env)


def _get_db_client() -> Client:
    client = Client()
    logger.info("authenticated with found service account")
    return client
