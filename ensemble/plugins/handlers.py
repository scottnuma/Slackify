from typing import Dict
from typing import Tuple

from slack import WebClient

from ensemble.channel_id import generate_channel_id
from ensemble.plugins import link_plugins
from ensemble.plugins import mention_plugins


def process_app_mention(web_client: WebClient, event_data: Dict):
    event, channel_id = parse_event_and_id(event_data)

    for mention_plugin in mention_plugins:
        if mention_plugin.matches(event):
            mention_plugin.handle(web_client, channel_id, event)


def process_link_shared(web_client: WebClient, event_data: Dict):
    event, channel_id = parse_event_and_id(event_data)

    for link_plugin in link_plugins:
        if link_plugin.matches(event):
            link_plugin.handle(web_client, channel_id, event)


def parse_event_and_id(event_data: Dict) -> Tuple[Dict, str]:
    event = event_data["event"]
    team_id = event_data["team_id"]
    channel = event["channel"]
    channel_id = generate_channel_id(team_id, channel)
    return event, channel_id
