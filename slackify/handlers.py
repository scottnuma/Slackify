"""
Process all slack link_shared events.

Distributes work to specific domain handlers, such as Spotify
"""

import logging
from . import spotify

logger = logging.getLogger(__name__)
domain_handlers = {'open.spotify.com': spotify.handler}


def handle_app_mention(slack_client, message, channel_id):
    """Give friendly response in thread when @mentioned."""
    if message.get("subtype") is None:
        text = message.get('text')
        if "hi" in text:
            logger.info("responding to message from %s", message["user"])
            response = ":notes:hi <@%s> :notes:" % message["user"]
            slack_client.api_call("chat.postMessage",
                                  channel=message["channel"],
                                  text=response,
                                  thread_ts=message['event_ts'])
        if "register channel" in text:
            logger.info("registering channel %s for %s",
                        channel_id.hex(), message["user"])
    else:
        logger.info("ignoring mention")


def link_handler(slack_client, slack_event, id):
    """Pass link events to their respective handlers and respond."""
    perfect_results = True
    for result in domain_handler(id, slack_event.get('links')):
        if result != spotify.ADD_SUCCESS:
            perfect_results = False
            slack_client.api_call(
                "chat.postMessage",
                channel=slack_event.get('channel'),
                text=result,
                thread_ts=slack_event.get('message_ts')
            )

    if perfect_results:
        slack_client.api_call(
            "reactions.add",
            channel=slack_event.get('channel'),
            name="notes",
            timestamp=slack_event.get('message_ts')
        )


def domain_handler(id, links):
    """Pass each link to their service's handler."""
    handler_feedback = []

    if not links:
        logger.info("ignoring empty links")
        return None

    if len(links) > 1:
        logger.info("multiple links given to handle_link")

    for link in links:
        domain = link.get('domain')
        if domain not in domain_handlers:
            logger.info("ignoring unrecognized domain: %s", domain)
            continue

        logger.info("passing link to domain handler")
        handler_feedback.append(domain_handlers[domain](id, link))

    return handler_feedback
