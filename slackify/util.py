import logging
import hashlib
import os

def init_logger():
    """Initialize logger with labeling and locations."""
    # create logger with 'spam_application'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')

    # create file handler which logs even debug messages
    fh = logging.FileHandler('slack_spotify_playlist.log')
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
    """Create an id unique to each channel regardless of workspace."""
    combined = "github.com/scottnuma" + str(team_id) + str(channel)
    return hashlib.sha224(combined.encode("utf-8")).digest()