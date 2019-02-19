import logging

logger = logging.getLogger(__name__)


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
