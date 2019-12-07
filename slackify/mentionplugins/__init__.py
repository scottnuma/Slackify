from typing import List

from slackify.mentionplugins.greeting import GreetingPlugin
from slackify.mentionplugins.plugin import MentionPlugin

mention_plugins: List[MentionPlugin] = [GreetingPlugin()]
