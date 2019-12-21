from typing import Dict
from typing import Tuple

from celery.utils.log import get_task_logger
from slack import WebClient

from ensemble import celery
from ensemble.channel_id import generate_channel_id
from ensemble.config import Config
from ensemble.plugins import link_plugins
from ensemble.plugins import mention_plugins

logger = get_task_logger(__name__)


@celery.task()
def process_app_mention(event_data: Dict):
    event, channel_id = parse_event_and_id(event_data)

    # We initialize the web client upon every call as we cannot store it
    # and pass it through for celery.
    web_client = WebClient(token=Config.SLACK_BOT_USER_OAUTH_ACCESS_TOKEN)

    for mention_plugin in mention_plugins:
        # logger.debug("matching app mention")

        if mention_plugin.matches(event):
            mention_plugin.handle(web_client, channel_id, event)


@celery.task()
def process_link_shared(event_data: Dict):
    event, channel_id = parse_event_and_id(event_data)
    web_client = WebClient(token=Config.SLACK_BOT_USER_OAUTH_ACCESS_TOKEN)

    for link_plugin in link_plugins:
        if link_plugin.matches(event):
            link_plugin.handle(web_client, channel_id, event)


def parse_event_and_id(event_data: Dict) -> Tuple[Dict, str]:
    event = event_data["event"]
    team_id = event_data["team_id"]
    channel = event["channel"]
    channel_id = generate_channel_id(team_id, channel)
    return event, channel_id
