import hashlib

from ensemble.config import Config


def generate_channel_id(team_id: str, channel: str) -> str:
    """
    Create an id unique to each channel regardless of workspace.

    Returns a hex string
    """
    dev_id = "github.com/scottnuma/ensemble"
    combined = "-".join([dev_id, team_id, channel, Config.SLACK_ID_KEY])
    return hashlib.sha224(combined.encode("utf-8")).digest().hex()
