from typing import List

from flask import Blueprint

from ensemble.plugins.example import ExampleLinkPlugin
from ensemble.plugins.example import ExampleMentionPlugin
from ensemble.plugins.plugin import Plugin
from ensemble.plugins.spotify import spotify_blueprints
from ensemble.plugins.spotify import spotify_mention_plugins

mention_plugins: List[Plugin] = [ExampleMentionPlugin]
mention_plugins += spotify_mention_plugins

link_plugins: List[Plugin] = [ExampleLinkPlugin]

plugin_blueprints: List[Blueprint] = []
plugin_blueprints += spotify_blueprints
