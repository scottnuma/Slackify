import hashlib
import logging
import os
import sys

from pythonjsonlogger import jsonlogger

from .settings import Config

logger = logging.getLogger(__name__)


def init_logger():
    """Initialize logger with labeling and locations."""
    # create logger with 'spam_application'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = jsonlogger.JsonFormatter()

    # create file handler which logs even debug messages
    fh = logging.FileHandler("_gen/slack_spotify_playlist.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # create console handle
    ch = logging.StreamHandler(sys.stdout)
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
    combined = "-".join([dev_id, team_id, channel, Config.SLACK_ID_KEY])
    return hashlib.sha224(combined.encode("utf-8")).digest().hex()
