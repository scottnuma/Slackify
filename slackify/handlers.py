"""
Process all slack link_shared events.

Distributes work to specific domain handlers, such as Spotify
"""
import logging
from typing import Dict
from typing import List
from typing import Optional

from slack import WebClient

from slackify.domainplugins import domain_plugins
from slackify.mentionplugins import mention_plugins
from slackify.settings import Config

logger = logging.getLogger(__name__)
# domain_handlers = {"open.spotify.com": spotify.handler}


def handle_app_mention(slack_client: WebClient, event: Dict, channel_id: str,) -> None:
    """Give friendly response in thread when @mentioned."""
    text = event["text"]

    for mention_plugin in mention_plugins:
        if mention_plugin.matches(text):
            mention_plugin.handle(
                slack_client, channel_id, event,
            )
            return
    logger.info('saw mention but found no key words in "%s"', text)


def handle_link(slack_client: WebClient, slack_event: Dict, channel_id: str,) -> None:
    """Pass link events to their respective handlers and respond."""
    # if not spotify.database.contains_channel(spotify.database.get_db(), channel_id):
    #    logger.info("ignoring message as channel not recognized")
    #    return

    links = slack_event.get("links")
    if not links:
        logger.info("ignoring empty links")
        return

    link = links[0]

    if len(links) > 1:
        logger.info("multiple links, ignoring links after the first.")

    feedback: Optional[str] = None

    domain = link.get("domain")
    for domain_plugin in domain_plugins:
        if domain_plugin.matches(domain):
            feedback = domain_plugin.handler(id, link)
            break

    if feedback is None:
        logger.info(f"found no plugin for {domain}")
        slack_client.reactions_add(
            channel=slack_event.get("channel"),
            name="notes",
            timestamp=slack_event.get("message_ts"),
        )
        return

    slack_client.chat_postMessage(
        channel=slack_event["channel"],
        text=feedback,
        thread_ts=slack_event["message_ts"],
    )
