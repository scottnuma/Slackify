import logging
import hashlib
import os

logger = logging.getLogger(__name__)

ID_SECRET_KEY = os.environ.get("SLACK_ID_KEY")
if not ID_SECRET_KEY:
    logger.warning("SLACK_ID_KEY environment variable not found")


def init_logger():
    """Initialize logger with labeling and locations."""
    # create logger with 'spam_application'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s")

    # create file handler which logs even debug messages
    fh = logging.FileHandler("slack_spotify_playlist.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # create console handle
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def generate_id(team_id, channel):
    """
    Create an id unique to each channel regardless of workspace.

    Returns a hex string
    """
    dev_id = "github.com/scottnuma"
    combined = "-".join([dev_id, team_id, channel, ID_SECRET_KEY])
    return hashlib.sha224(combined.encode("utf-8")).digest().hex()
