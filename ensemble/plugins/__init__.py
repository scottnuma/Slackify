from typing import List

from ensemble.plugins.example import ExampleLinkPlugin
from ensemble.plugins.example import ExampleMentionPlugin
from ensemble.plugins.plugin import Plugin

mention_plugins: List[Plugin] = [ExampleMentionPlugin]
link_plugins: List[Plugin] = [ExampleLinkPlugin]
