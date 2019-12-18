from typing import List

from slackify.tasks.mentionplugins.greeting import GreetingPlugin
from slackify.tasks.mentionplugins.plugin import MentionPlugin

mention_plugins: List[MentionPlugin] = [GreetingPlugin()]
